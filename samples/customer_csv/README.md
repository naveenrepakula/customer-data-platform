# Customer CSV Samples

Reusable synthetic CSV files for local and DEV validation testing. These files contain no real customer data.

## Files

- `valid_customer.csv`: Valid header containing all required columns.
- `missing_phone_number.csv`: Invalid header missing the required `phone_number` column.
- `duplicate_email.csv`: Invalid header containing the `email` column twice.
- `duplicate_email_whitespace.csv`: Invalid header where `email` and ` email ` become duplicates after whitespace normalization.

## Expected Results

| File | is_valid | missing_columns | duplicate_columns |
| --- | --- | --- | --- |
| `valid_customer.csv` | `true` | `[]` | `[]` |
| `missing_phone_number.csv` | `false` | `["phone_number"]` | `[]` |
| `duplicate_email.csv` | `false` | `[]` | `["email"]` |
| `duplicate_email_whitespace.csv` | `false` | `[]` | `["email"]` |
