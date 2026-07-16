from typing import Dict, List

REQUIRED_COLUMNS = [
    "customer_id",
    "customer_name",
    "email",
    "created_at",
    "phone_number",
]


def validate_csv_header(header: List[str]) -> Dict[str, object]:
    normalized_header = [column.strip() for column in header]

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in normalized_header
    ]

    return {
        "is_valid": len(missing) == 0,
        "missing_columns": missing,
    }
