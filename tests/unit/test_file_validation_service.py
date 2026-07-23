from src.services.file_validation_service import validate_csv_header

def test_validate_csv_header_success():
    header =[
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
