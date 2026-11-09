
# Employee API Documentation

## Endpoints

### 1. Health Check
GET /health

Returns API status.

Expected response:
{"status": "ok"}

### 2. Get All Employees
GET /employees

Returns all employee records.

### 3. Get Employee by Name
GET /employees/{name}

Returns employee details.

Returns 404 if employee is not found.

### 4. Add Employee
POST /employees

Example request:

{
    "name": "Ravi",
    "salary": 50000
}

Name cannot be empty.
Salary must be greater than zero.

Returns 422 for invalid input.
