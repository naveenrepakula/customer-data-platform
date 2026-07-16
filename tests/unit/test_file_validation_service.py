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
