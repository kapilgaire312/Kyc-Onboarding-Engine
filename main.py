from datetime import date

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator


class Customer_Info(BaseModel):
    name: str = Field(min_length=3)
    dob: date
    citizenship_no: str = Field(pattern=r"\d{2}-\d{2}-\d{2}-\d{5}")
    citizenship_issue_date: date

    # field validator to check age is atleast 18
    @field_validator("dob", mode="after")
    @classmethod
    def ensure_18_plus(cls, dob: date):
        today = date.today()

        # check year
        age = today.year - dob.year

        # check month and day
        if (today.month, today.day) < (dob.month, dob.day):
            age = age - 1

        if age < 18:
            raise ValueError("Customer must be at least 18 years old.")

        return dob

    # field validator to ensure date of issue is not in future
    @field_validator("citizenship_issue_date", mode="after")
    @classmethod
    def ensure_valid_issue_date(cls, issue_date: date):
        today = date.today()
        if issue_date > today:
            raise ValueError("Citizenship issue date cannot be in future.")


app = FastAPI()


# Custom handle the pydantic validation errror
# it is converted to RequestValidationError by fastapi


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(exc.errors())
    errors = []
    for error in exc.errors():
        errors.append({"field": f"{error['loc'][1]}", "message": error["msg"]})

    return JSONResponse(
        status_code=422, content={"message": "Unprocessable Entity", "errors": errors}
    )


# Allow all origins, methods, and headers for testing with html file
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(path="/")
def read_root():
    return {"message": "hello "}


@app.post("/api/v1/kyc/verify")
def add_user(customer_data: Customer_Info):
    print(customer_data.model_dump())
    return {"message": "success"}
