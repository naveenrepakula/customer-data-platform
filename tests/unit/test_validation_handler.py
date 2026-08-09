import importlib
import json
from unittest.mock import patch

handler = importlib.import_module("lambda.validation.handler")


def test_lambda_handler_success():
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": "cdp-raw-dev",
                    },
                    "object": {
                        "key": "customer/customer+sample.csv",
                    },
                }
            }
        ]
    }

    csv_header = [
        "customer_id",
        "customer_name",
        "email",
        "created_at",
        "phone_number",
    ]

    csv_rows = [
        [
            "CUST001",
            "Naveen",
            "naveen@example.com",
            "2026-07-14",
            "9999999999",
        ],
    ]

    with patch.object(
        handler,
        "read_csv_from_s3",
        return_value=(csv_header, csv_rows),
    ) as mock_read_csv:
        response = handler.lambda_handler(event, None)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {
        "message": "Validation successful",
    }

    mock_read_csv.assert_called_once_with(
        bucket_name="cdp-raw-dev",
        object_key="customer/customer sample.csv",
    )


def test_lambda_handler_missing_required_column():
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": "cdp-raw-dev",
                    },
                    "object": {
                        "key": "customer/invalid_customer.csv",
                    },
                }
            }
        ]
    }

    csv_header = [
        "customer_id",
        "customer_name",
        "email",
        "created_at",
    ]

    csv_rows = []

    with patch.object(
        handler,
        "read_csv_from_s3",
        return_value=(csv_header, csv_rows),
    ):
        response = handler.lambda_handler(event, None)

    response_body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert response_body["is_valid"] is False
    assert "phone_number" in response_body["missing_columns"]


def test_lambda_handler_empty_csv():
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": "cdp-raw-dev",
                    },
                    "object": {
                        "key": "customer/empty.csv",
                    },
                }
            }
        ]
    }

    with patch.object(
        handler,
        "read_csv_from_s3",
        side_effect=ValueError("CSV file is empty"),
    ):
        response = handler.lambda_handler(event, None)

    assert response["statusCode"] == 400
    assert json.loads(response["body"]) == {
        "message": "CSV file is empty",
    }


def test_lambda_handler_blank_customer_id():
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": "cdp-raw-dev",
                    },
                    "object": {
                        "key": "customer/blank_customer_id.csv",
                    },
                }
            }
        ]
    }

    csv_header = [
        "customer_id",
        "customer_name",
        "email",
        "created_at",
        "phone_number",
    ]

    csv_rows = [
        [
            "CUST001",
            "Alice",
            "alice@example.com",
            "2026-08-04",
            "9876543210",
        ],
        [
            "",
            "Bob",
            "bob@example.com",
            "2026-08-04",
            "9876543211",
        ],
    ]

    with patch.object(
        handler,
        "read_csv_from_s3",
        return_value=(csv_header, csv_rows),
    ):
        response = handler.lambda_handler(event, None)

    response_body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert response_body["is_valid"] is False
    assert response_body["blank_customer_id_rows"] == [3]


def test_lambda_handler_incorrect_row_column_count():
    # Arrange
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": "cdp-raw-dev",
                    },
                    "object": {
                        "key": "customer/incorrect_column_count.csv",
                    },
                }
            }
        ]
    }

    csv_header = [
        "customer_id",
        "customer_name",
        "email",
        "created_at",
        "phone_number",
    ]

    csv_rows = [
        [
            "CUST001",
            "Alice",
            "alice@example.com",
            "2026-08-08",
            "9876543210",
        ],
        [
            "CUST002",
            "Bob",
            "bob@example.com",
        ],
    ]

    # Act
    with patch.object(
        handler,
        "read_csv_from_s3",
        return_value=(csv_header, csv_rows),
    ):
        response = handler.lambda_handler(event, None)

    response_body = json.loads(response["body"])

    # Assert
    assert response["statusCode"] == 400
    assert response_body["is_valid"] is False
    assert response_body["incorrect_column_count_rows"] == [3]
