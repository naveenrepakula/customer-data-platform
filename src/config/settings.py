import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    env: str = os.getenv("ENV", "dev")
    aws_region: str = os.getenv("AWS_REGION", "ap-south-1")
    raw_bucket: str = os.getenv("RAW_BUCKET", "cdp-raw-dev")
    processed_bucket: str = os.getenv("PROCESSED_BUCKET", "cdp-processed-dev")

settings = Settings()
