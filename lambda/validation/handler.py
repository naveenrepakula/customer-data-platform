import json
import sys
from pathlib import Path
from urllib.parse import unquote_plus

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from src.common.logger import get_logger
from src.services.file_validation_service import validate_csv_header
from src.services.s3_csv_service import read_csv_header_from_s3

logger = get_logger(__name__)


def lambda_handler(event, context):
    logger.info("Lambda validation started")
    logger.info("Received event: %s", json.dumps(event))

    record = event["Records"][0]

    bucket_name = record["s3"]["bucket"]["name"]
    object_key = unquote_plus(record["s3"]["object"]["key"])

    logger.info(
        "Reading CSV header from s3://%s/%s",
        bucket_name,
        object_key,
    )

    try:
        csv_header = read_csv_header_from_s3(
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

    result = validate_csv_header(csv_header)

    if not result["is_valid"]:
        logger.error("Validation failed: %s", result)

        return {
            "statusCode": 400,
            "body": json.dumps(result),
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