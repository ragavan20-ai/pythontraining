
import json
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

BASE_DIR = Path(__file__).resolve().parent.parent
EMPLOYEES_FILE = BASE_DIR / "config" / "employees.json"

app = FastAPI(title="Employee API")


class Employee(BaseModel):
    name: str = Field(min_length=1)
    salary: float = Field(gt=0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value


def read_employees() -> List[dict]:
    with open(EMPLOYEES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_employees(employees: List[dict]) -> None:
    with open(EMPLOYEES_FILE, "w", encoding="utf-8") as file:
        json.dump(employees, file, indent=4)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/employees")
def get_employees() -> List[dict]:
    return read_employees()


@app.get("/employees/{name}")
def get_employee(name: str) -> dict:
    employees = read_employees()

    for employee in employees:
        if employee["name"].lower() == name.lower():
            return employee

    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees", status_code=201)
def create_employee(employee: Employee) -> dict:
    employees = read_employees()

    for existing in employees:
        if existing["name"].lower() == employee.name.lower():
            raise HTTPException(
                status_code=409,
                detail="Employee already exists",
            )

    new_employee = employee.model_dump()
    employees.append(new_employee)
    save_employees(employees)

    return new_employee
