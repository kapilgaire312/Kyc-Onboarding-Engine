from datetime import date

from fastapi import FastAPI
from pydantic import BaseModel, Field, ValidationError, field_validator


class Customer_Info(BaseModel):
    name: str = Field(min_length=3)
    Dob: date
    citizenship_no: str = Field(pattern=r"\d{2}-\d{2}-\d{2}-\d{5}")
    address: str = Field(min_length=5)
    citizenship_issue_date: date

    # field validator to check age is atleast 18
    @field_validator("Dob", mode="after")
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


@app.get(path="/")
def read_root():
    return {"message": "hello "}


@app.put("/new_user")
def add_user(customer_data: Customer_Info):
    print(customer_data.model_dump())
    return {"message": "success"}
