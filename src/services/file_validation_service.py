
REQUIRED_COLUMNS = [
    "customer_id",
    "customer_name",
    "email",
    "created_at",
    "phone_number",
]


def validate_csv_header(header: list[str]) -> dict[str, object]:
    normalized_header = [column.strip() for column in header]

    is_column_order_valid = normalized_header == REQUIRED_COLUMNS

    missing = [column for column in REQUIRED_COLUMNS if column not in normalized_header]

    unexpected = [
        column
        for column in normalized_header
        if column != "" and column not in REQUIRED_COLUMNS
    ]

    blank_positions = [
        position
        for position, column in enumerate(normalized_header, start=1)
        if column == ""
    ]

    seen = set()
    duplicates = []

    for column in normalized_header:
        if column == "":
            continue

        if column in seen and column not in duplicates:
            duplicates.append(column)

        seen.add(column)

    return {
        "is_valid": (
            len(missing) == 0
            and len(unexpected) == 0
            and len(duplicates) == 0
            and len(blank_positions) == 0
            and is_column_order_valid
        ),
        "is_column_order_valid": is_column_order_valid,
        "missing_columns": missing,
        "unexpected_columns": unexpected,
        "duplicate_columns": duplicates,
        "blank_column_positions": blank_positions,
    }


def validate_customer_id_rows(
    rows: list[list[str]],
) -> dict[str, object]:
    blank_customer_id_rows = [
        line_number
        for line_number, row in enumerate(rows, start=2)
        if not row or row[0].strip() == ""
    ]

    return {
        "is_valid": len(blank_customer_id_rows) == 0,
        "blank_customer_id_rows": blank_customer_id_rows,
    }
