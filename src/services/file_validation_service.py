from collections import defaultdict
from datetime import date

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


def validate_row_column_count(
    rows: list[list[str]],
    expected_column_count: int,
) -> dict[str, object]:
    incorrect_column_count_rows = [
        line_number
        for line_number, row in enumerate(rows, start=2)
        if len(row) != expected_column_count
    ]

    return {
        "is_valid": len(incorrect_column_count_rows) == 0,
        "incorrect_column_count_rows": incorrect_column_count_rows,
    }


def validate_duplicate_customer_ids(
    rows: list[list[str]],
) -> dict[str, object]:
    customer_id_to_rows: dict[str, list[int]] = defaultdict(list)

    for line_number, row in enumerate(rows, start=2):
        if not row:
            continue

        customer_id = row[0].strip()

        if customer_id == "":
            continue

        customer_id_to_rows[customer_id].append(line_number)

    duplicate_customer_id_rows = sorted(
        line_number
        for line_numbers in customer_id_to_rows.values()
        if len(line_numbers) > 1
        for line_number in line_numbers
    )

    return {
        "is_valid": len(duplicate_customer_id_rows) == 0,
        "duplicate_customer_id_rows": duplicate_customer_id_rows,
    }


def validate_created_at_rows(
    rows: list[list[str]],
) -> dict[str, object]:
    invalid_created_at_rows = []

    for line_number, row in enumerate(rows, start=2):
        if len(row) <= 3:
            continue

        created_at = row[3].strip()

        if created_at == "":
            continue

        try:
            date.fromisoformat(created_at)
        except ValueError:
            invalid_created_at_rows.append(line_number)

    return {
        "is_valid": len(invalid_created_at_rows) == 0,
        "invalid_created_at_rows": invalid_created_at_rows,
    }


def validate_email_rows(
    rows: list[list[str]],
) -> dict[str, object]:
    invalid_email_rows = []

    for line_number, row in enumerate(rows, start=2):
        if len(row) <= 2:
            continue

        email = row[2].strip()

        if email == "":
            continue

        if "@" not in email:
            invalid_email_rows.append(line_number)
            continue

        local_part, domain = email.rsplit("@", 1)

        if local_part == "" or domain == "":
            invalid_email_rows.append(line_number)
            continue

        if "." not in domain or domain.startswith(".") or domain.endswith("."):
            invalid_email_rows.append(line_number)

    return {
        "is_valid": len(invalid_email_rows) == 0,
        "invalid_email_rows": invalid_email_rows,
    }
