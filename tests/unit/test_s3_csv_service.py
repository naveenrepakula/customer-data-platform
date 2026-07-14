from unittest.mock import Mock

import pytest

from src.services.s3_csv_service import read_csv_header_from_s3


def test_read_csv_header_from_s3_success():
    s3_client = Mock()
    response_body = Mock()

    response_body.iter_lines.return_value = iter(
        [
            b"customer_id,customer_name,email,created_at,phone_number",
            b"1,Naveen,naveen@example.com,2026-07-14,9999999999",
        ]
    )

    s3_client.get_object.return_value = {
        "Body": response_body,
    }

    header = read_csv_header_from_s3(
        bucket_name="cdp-raw-dev",
        object_key="customer/customer_sample.csv",
        s3_client=s3_client,
    )

    assert header == [
        "customer_id",
        "customer_name",
        "email",
        "created_at",
        "phone_number",
    ]

    s3_client.get_object.assert_called_once_with(
        Bucket="cdp-raw-dev",
        Key="customer/customer_sample.csv",
    )

    response_body.iter_lines.assert_called_once_with()
    response_body.read.assert_not_called()


def test_read_csv_header_from_s3_empty_file():
    s3_client = Mock()
    response_body = Mock()

    response_body.iter_lines.return_value = iter([])

    s3_client.get_object.return_value = {
        "Body": response_body,
    }

    with pytest.raises(ValueError, match="CSV file is empty"):
        read_csv_header_from_s3(
            bucket_name="cdp-raw-dev",
            object_key="customer/empty.csv",
            s3_client=s3_client,
        )