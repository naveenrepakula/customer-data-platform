from src.services.file_validation_service import (
    validate_csv_header,
    validate_customer_id_rows,
    validate_duplicate_customer_ids,
    validate_row_column_count,
)


def test_validate_csv_header_success():
    header = [
        "customer_id",
        "customer_name",
        "email",
        "created_at",
        "phone_number",
    ]
    result = validate_csv_header(header)
    assert result["is_valid"] is True
    assert result["missing_columns"] == []
    assert result["duplicate_columns"] == []
    assert result["blank_column_positions"] == []
    assert result["unexpected_columns"] == []
    assert result["is_column_order_valid"] is True


def test_validate_csv_header_missing_column():
    header = ["customer_id", "customer_name"]
    result = validate_csv_header(header)
    assert result["is_valid"] is False
    assert "email" in result["missing_columns"]
    assert "phone_number" in result["missing_columns"]


def test_validate_csv_header_with_whitespace():
    header = [
        "customer_id",
        " customer_name ",
        " email ",
        " created_at ",
        " phone_number ",
    ]

    result = validate_csv_header(header)

    assert result["is_valid"] is True
    assert result["missing_columns"] == []


def test_validate_csv_header_with_duplicate_column():
    header = [
        "customer_id",
        "customer_name",
        "email",
        "email",
        "created_at",
        "phone_number",
    ]

    result = validate_csv_header(header)

    assert result["is_valid"] is False
    assert result["missing_columns"] == []
    assert result["duplicate_columns"] == ["email"]


def test_validate_csv_header_with_duplicate_after_whitespace_normalization():
    header = [
        "customer_id",
        "customer_name",
        "email",
        " email ",
        "created_at",
        "phone_number",
    ]

    result = validate_csv_header(header)

    assert result["is_valid"] is False
    assert result["missing_columns"] == []
    assert result["duplicate_columns"] == ["email"]


def test_validate_csv_header_with_blank_column_name():
    # Arrange
    header = [
        "customer_id",
        "customer_name",
        "email",
        "",
        "created_at",
        "phone_number",
    ]

    # Act
    result = validate_csv_header(header)

    # Assert
    assert result["is_valid"] is False
    assert result["missing_columns"] == []
    assert result["duplicate_columns"] == []
    assert result["blank_column_positions"] == [4]


def test_validate_csv_header_with_whitespace_only_column_name():
    # Arrange
    header = [
        "customer_id",
        "customer_name",
        "email",
        "   ",
        "created_at",
        "phone_number",
    ]

    # Act
    result = validate_csv_header(header)

    # Assert
    assert result["is_valid"] is False
    assert result["missing_columns"] == []
    assert result["duplicate_columns"] == []
    assert result["blank_column_positions"] == [4]


def test_validate_csv_header_with_unexpected_column():
    # Arrange
    header = [
        "customer_id",
        "customer_name",
        "email",
        "created_at",
        "phone_number",
        "address",
    ]

    # Act
    result = validate_csv_header(header)

    # Assert
    assert result["is_valid"] is False
    assert result["missing_columns"] == []
    assert result["duplicate_columns"] == []
    assert result["blank_column_positions"] == []
    assert result["unexpected_columns"] == ["address"]


def test_validate_csv_header_with_unexpected_column_after_whitespace_normalization():
    # Arrange
    header = [
        "customer_id",
        "customer_name",
        "email",
        "created_at",
        "phone_number",
        " address ",
    ]

    # Act
    result = validate_csv_header(header)

    # Assert
    assert result["is_valid"] is False
    assert result["missing_columns"] == []
    assert result["duplicate_columns"] == []
    assert result["blank_column_positions"] == []
    assert result["unexpected_columns"] == ["address"]


def test_validate_csv_header_with_incorrect_column_order():
    # Arrange
    header = [
        "email",
        "customer_id",
        "customer_name",
        "created_at",
        "phone_number",
    ]

    # Act
    result = validate_csv_header(header)

    # Assert
    assert result["is_valid"] is False
    assert result["is_column_order_valid"] is False
    assert result["missing_columns"] == []
    assert result["unexpected_columns"] == []
    assert result["duplicate_columns"] == []
    assert result["blank_column_positions"] == []


def test_validate_customer_id_rows_with_empty_customer_id():
    # Arrange
    rows = [
        ["CUST001", "Alice", "alice@example.com", "2026-08-04", "9876543210"],
        ["", "Bob", "bob@example.com", "2026-08-04", "9876543211"],
    ]

    # Act
    result = validate_customer_id_rows(rows)

    # Assert
    assert result["is_valid"] is False
    assert result["blank_customer_id_rows"] == [3]


def test_validate_customer_id_rows_with_whitespace_only_customer_id():
    # Arrange
    rows = [
        ["CUST001", "Alice", "alice@example.com", "2026-08-04", "9876543210"],
        ["   ", "Bob", "bob@example.com", "2026-08-04", "9876543211"],
    ]

    # Act
    result = validate_customer_id_rows(rows)

    # Assert
    assert result["is_valid"] is False
    assert result["blank_customer_id_rows"] == [3]


def test_validate_customer_id_rows_with_multiple_blank_customer_ids():
    # Arrange
    rows = [
        ["CUST001", "Alice", "alice@example.com", "2026-08-04", "9876543210"],
        ["", "Bob", "bob@example.com", "2026-08-04", "9876543211"],
        ["CUST003", "Charlie", "charlie@example.com", "2026-08-04", "9876543212"],
        ["   ", "David", "david@example.com", "2026-08-04", "9876543213"],
    ]

    # Act
    result = validate_customer_id_rows(rows)

    # Assert
    assert result["is_valid"] is False
    assert result["blank_customer_id_rows"] == [3, 5]


def test_validate_customer_id_rows_success():
    # Arrange
    rows = [
        ["CUST001", "Alice", "alice@example.com", "2026-08-04", "9876543210"],
        ["CUST002", "Bob", "bob@example.com", "2026-08-04", "9876543211"],
    ]

    # Act
    result = validate_customer_id_rows(rows)

    # Assert
    assert result["is_valid"] is True
    assert result["blank_customer_id_rows"] == []


def test_validate_row_column_count_with_too_few_columns():
    # Arrange
    rows = [
        [
            "CUST001",
            "Alice",
            "alice@example.com",
            "2026-08-08",
            "9876543210",
        ],
        [
            "CUST002",
            "Bob",
            "bob@example.com",
        ],
    ]

    # Act
    result = validate_row_column_count(
        rows,
        expected_column_count=5,
    )

    # Assert
    assert result["is_valid"] is False
    assert result["incorrect_column_count_rows"] == [3]


def test_validate_row_column_count_with_too_many_columns():
    # Arrange
    rows = [
        [
            "CUST001",
            "Alice",
            "alice@example.com",
            "2026-08-08",
            "9876543210",
        ],
        [
            "CUST002",
            "Bob",
            "bob@example.com",
            "2026-08-08",
            "9876543211",
            "EXTRA",
        ],
    ]

    # Act
    result = validate_row_column_count(
        rows,
        expected_column_count=5,
    )

    # Assert
    assert result["is_valid"] is False
    assert result["incorrect_column_count_rows"] == [3]


def test_validate_row_column_count_with_multiple_incorrect_rows():
    # Arrange
    rows = [
        [
            "CUST001",
            "Alice",
            "alice@example.com",
            "2026-08-08",
            "9876543210",
        ],
        [
            "CUST002",
            "Bob",
            "bob@example.com",
        ],
        [
            "CUST003",
            "Charlie",
            "charlie@example.com",
            "2026-08-08",
            "9876543212",
        ],
        [
            "CUST004",
            "David",
            "david@example.com",
            "2026-08-08",
            "9876543213",
            "EXTRA",
        ],
    ]

    # Act
    result = validate_row_column_count(
        rows,
        expected_column_count=5,
    )

    # Assert
    assert result["is_valid"] is False
    assert result["incorrect_column_count_rows"] == [3, 5]


def test_validate_row_column_count_success():
    # Arrange
    rows = [
        [
            "CUST001",
            "Alice",
            "alice@example.com",
            "2026-08-08",
            "9876543210",
        ],
        [
            "CUST002",
            "Bob",
            "bob@example.com",
            "2026-08-08",
            "9876543211",
        ],
    ]

    # Act
    result = validate_row_column_count(
        rows,
        expected_column_count=5,
    )

    # Assert
    assert result["is_valid"] is True
    assert result["incorrect_column_count_rows"] == []


def test_validate_duplicate_customer_ids_with_one_duplicate():
    # Arrange
    rows = [
        [
            "CUST001",
            "Alice",
            "alice@example.com",
            "2026-08-08",
            "9876543210",
        ],
        [
            "CUST001",
            "Bob",
            "bob@example.com",
            "2026-08-08",
            "9876543211",
        ],
    ]

    # Act
    result = validate_duplicate_customer_ids(rows)
    # Assert
    assert result["is_valid"] is False
    assert result["duplicate_customer_id_rows"] == [2, 3]


def test_validate_duplicate_customer_ids_success():
    # Arrange
    rows = [
        [
            "CUST001",
            "Alice",
            "alice@example.com",
            "2026-08-08",
            "9876543210",
        ],
        [
            "CUST002",
            "Bob",
            "bob@example.com",
            "2026-08-08",
            "9876543211",
        ],
    ]

    # Act
    result = validate_duplicate_customer_ids(rows)

    # Assert
    assert result["is_valid"] is True
    assert result["duplicate_customer_id_rows"] == []


def test_validate_duplicate_customer_ids_with_same_id_multiple_times():
    # Arrange
    rows = [
        [
            "CUST001",
            "Alice",
            "alice@example.com",
            "2026-08-08",
            "9876543210",
        ],
        [
            "CUST002",
            "Bob",
            "bob@example.com",
            "2026-08-08",
            "9876543211",
        ],
        [
            "CUST001",
            "Charlie",
            "charlie@example.com",
            "2026-08-08",
            "9876543212",
        ],
        [
            "CUST001",
            "David",
            "david@example.com",
            "2026-08-08",
            "9876543213",
        ],
    ]

    # Act
    result = validate_duplicate_customer_ids(rows)

    # Assert
    assert result["is_valid"] is False
    assert result["duplicate_customer_id_rows"] == [2, 4, 5]


def test_validate_duplicate_customer_ids_with_multiple_duplicate_ids():
    # Arrange
    rows = [
        [
            "CUST001",
            "Alice",
            "alice@example.com",
            "2026-08-08",
            "9876543210",
        ],
        [
            "CUST002",
            "Bob",
            "bob@example.com",
            "2026-08-08",
            "9876543211",
        ],
        [
            "CUST001",
            "Charlie",
            "charlie@example.com",
            "2026-08-08",
            "9876543212",
        ],
        [
            "CUST002",
            "David",
            "david@example.com",
            "2026-08-08",
            "9876543213",
        ],
    ]

    # Act
    result = validate_duplicate_customer_ids(rows)

    # Assert
    assert result["is_valid"] is False
    assert result["duplicate_customer_id_rows"] == [2, 3, 4, 5]
