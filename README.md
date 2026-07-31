# KYC Onboarding Practice Project

A small FastAPI project built to practice **Pydantic validation** and **API routing**.

This project focuses on a simple KYC-style verification flow where incoming data is strictly validated before it is accepted. It is meant as a learning project and a GitHub practice repo, not a production-ready onboarding system.

## What It Demonstrates

- FastAPI routing with `GET` and `POST` endpoints
- Pydantic request models with field validation
- Custom validation error responses
- A simple HTML form for testing the API manually

## Tech Stack

- Python
- FastAPI
- Pydantic
- HTML / JavaScript for the demo form

## Project Files

- `main.py` - FastAPI app, request model, and validation logic
- `index.html` - Basic frontend form that sends test requests to the API

## Run the Project

1. Install the dependencies:

```bash
pip install -e .
```

2. Start the FastAPI server:

```bash
fastapi dev main.py
```

3. Open the demo form in `index.html` and submit data to the API.

## API Endpoints

### `GET /`

Returns a simple welcome message.

### `POST /api/v1/kyc/verify`

Validates a KYC request body and returns success when the payload passes all checks.

## Validation Rules

The request body expects:

- `name`: at least 3 characters
- `dob`: must make the customer at least 18 years old
- `citizenship_no`: must match the pattern `NN-NN-NN-NNNNN`
- `citizenship_issue_date`: cannot be in the future

If validation fails, the API returns a custom `422 Unprocessable Entity` response with the field-level errors.

## Example Payload

```json
{
	"name": "John Doe",
	"dob": "1995-04-12",
	"citizenship_no": "12-34-56-78901",
	"citizenship_issue_date": "2020-06-15"
}
```

## Notes

- This project is intentionally small and focused on validation behavior.
- The demo frontend sends requests to `http://localhost:8000/api/v1/kyc/verify`.
