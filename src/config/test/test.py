
import json

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_file = tmp_path / "employees.json"

    employees = [
        {"name": "Ravi", "salary": 50000},
        {"name": "Priya", "salary": 45000},
    ]

    test_file.write_text(json.dumps(employees), encoding="utf-8")
    monkeypatch.setattr(app_module, "EMPLOYEES_FILE", test_file)

    return TestClient(app_module.app)


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_employee_list(client):
    response = client.get("/employees")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_employee_success(client):
    response = client.get("/employees/Ravi")
    assert response.status_code == 200
    assert response.json()["name"] == "Ravi"


def test_employee_not_found(client):
    response = client.get("/employees/Unknown")
    assert response.status_code == 404


def test_invalid_salary(client):
    response = client.post(
        "/employees",
        json={"name": "Ravi2", "salary": -5},
    )
    assert response.status_code == 422


def test_empty_name(client):
    response = client.post(
        "/employees",
        json={"name": "   ", "salary": 30000},
    )
    assert response.status_code == 422


def test_create_employee_success(client):
    response = client.post(
        "/employees",
        json={"name": "Kumar", "salary": 55000},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Kumar"


def test_duplicate_employee(client):
    response = client.post(
        "/employees",
        json={"name": "Ravi", "salary": 60000},
    )
    assert response.status_code == 409

