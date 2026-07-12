from typing import Dict, List

REQUIRED_COLUMNS = [
    "customer_id",
    "customer_name",
    "email",
    "created_at",
    "phone_number",
]

def validate_csv_header(header: List[str]) -> Dict[str, object]:
    missing = [col for col in REQUIRED_COLUMNS if col not in header]
    return {
        "is_valid": len(missing) == 0,
        "missing_columns": missing,
    }
