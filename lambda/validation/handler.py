import json
import sys
from pathlib import Path
from urllib.parse import unquote_plus

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from src.common.logger import get_logger
from src.services.file_validation_service import (
    validate_csv_header,
    validate_customer_id_rows,
)
from src.services.s3_csv_service import read_csv_from_s3

logger = get_logger(__name__)


def lambda_handler(event, context):
    logger.info("Lambda validation started")
    logger.info("Received event: %s", json.dumps(event))

    record = event["Records"][0]

    bucket_name = record["s3"]["bucket"]["name"]
    object_key = unquote_plus(record["s3"]["object"]["key"])

    logger.info(
        "Reading CSV from s3://%s/%s",
        bucket_name,
        object_key,
    )

    try:
        csv_header, csv_rows = read_csv_from_s3(
            bucket_name=bucket_name,
            object_key=object_key,
        )
    except ValueError as error:
        logger.error("Validation failed: %s", error)

        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": str(error),
                }
            ),
        }

    header_result = validate_csv_header(csv_header)

    if not header_result["is_valid"]:
        logger.error("Header validation failed: %s", header_result)

        return {
            "statusCode": 400,
            "body": json.dumps(header_result),
        }
    logger.info("Header validation successful")

    row_result = validate_customer_id_rows(csv_rows)

    if not row_result["is_valid"]:
        logger.error("Row validation failed: %s", row_result)

        return {
            "statusCode": 400,
            "body": json.dumps(row_result),
        }

    logger.info("Validation successful")

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Validation successful",
            }
        ),
    }
