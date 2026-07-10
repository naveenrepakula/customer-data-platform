import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from src.common.logger import get_logger
from src.services.file_validation_service import validate_csv_header

logger = get_logger(__name__)

def lambda_handler(event, context):
    logger.info("Lambda validation started")
    logger.info("Received event: %s", json.dumps(event))

    sample_header = ["customer_id", "customer_name", "email", "created_at"]
    result = validate_csv_header(sample_header)

    if not result["is_valid"]:
        logger.error("Validation failed: %s", result)
        return {"statusCode": 400, "body": json.dumps(result)}

    logger.info("Validation successful")
    return {"statusCode": 200, "body": json.dumps({"message": "Validation successful"})}

if __name__ == "__main__":
    test_event = {
        "Records": [
            {"s3": {"bucket": {"name": "cdp-raw-dev"}, "object": {"key": "customer/customer_sample.csv"}}}
        ]
    }
    print(lambda_handler(test_event, None))
