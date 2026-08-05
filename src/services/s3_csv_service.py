import csv
from typing import Any

import boto3

_default_s3_client = boto3.client("s3")


def read_csv_header_from_s3(
    bucket_name: str,
    object_key: str,
    s3_client: Any = None,
) -> list[str]:
    client = s3_client if s3_client is not None else _default_s3_client

    response = client.get_object(
        Bucket=bucket_name,
        Key=object_key,
    )

    first_line = next(response["Body"].iter_lines(), None)

    if not first_line:
        raise ValueError("CSV file is empty")

    decoded_header = first_line.decode("utf-8-sig")
    return next(csv.reader([decoded_header]))


def read_csv_from_s3(
    bucket_name: str,
    object_key: str,
    s3_client: Any = None,
) -> tuple[list[str], list[list[str]]]:
    client = s3_client if s3_client is not None else _default_s3_client

    response = client.get_object(
        Bucket=bucket_name,
        Key=object_key,
    )

    decoded_lines = (line.decode("utf-8-sig") for line in response["Body"].iter_lines())

    csv_rows = list(csv.reader(decoded_lines))

    if not csv_rows:
        raise ValueError("CSV file is empty")
    header = csv_rows[0]
    rows = csv_rows[1:]
    return header, rows
