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

    seen = set()
    duplicates = []

    for column in normalized_header:
        if column in seen and column not in duplicates:
            duplicates.append(column)

        seen.add(column)

    return {
        "is_valid": len(missing) == 0 and len(duplicates) == 0,
        "missing_columns": missing,
        "duplicate_columns": duplicates,
    }
