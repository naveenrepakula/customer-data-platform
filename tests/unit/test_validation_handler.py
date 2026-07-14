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

    with patch.object(
        handler,
        "read_csv_header_from_s3",
        return_value=csv_header,
    ) as mock_read_csv_header:
        response = handler.lambda_handler(event, None)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {
        "message": "Validation successful",
    }

    mock_read_csv_header.assert_called_once_with(
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

    with patch.object(
        handler,
        "read_csv_header_from_s3",
        return_value=csv_header,
    ):
        response = handler.lambda_handler(event, None)

    response_body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert response_body["is_valid"] is False
    assert "phone_number" in response_body["missing_columns"]