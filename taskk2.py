
import csv
import json
import logging
from pathlib import Path
from typing import List, Optional, Union

import openpyxl
import fitz


# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# Convert salary into integer
def convert_salary(value: Union[int, str]) -> int:
    return int(value)


# Read employees from CSV
def read_employees(path: Union[str, Path]) -> List[dict]:
    with open(path, "r", newline="") as file:
        reader = csv.DictReader(file)
        employees = list(reader)

    for employee in employees:
        employee["salary"] = convert_salary(employee["salary"])

    return employees


# Write employees into JSON
def write_json(employees: List[dict]) -> None:
    with open("employees.json", "w") as file:
        json.dump({"employees": employees}, file, indent=4)


# Write high earners into CSV
def write_high_earners(employees: List[dict]) -> int:
    high_earners = [
        emp for emp in employees if emp["salary"] > 50000
    ]

    with open("high_earners.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["name", "department", "salary"]
        )
        writer.writeheader()
        writer.writerows(high_earners)

    return len(high_earners)


# Create Excel file and read it back
def create_excel(employees: List[dict]) -> int:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Employees"

    sheet.append(["Name", "Department", "Salary"])

    for emp in employees:
        sheet.append([
            emp["name"],
            emp["department"],
            emp["salary"]
        ])

    workbook.save("salary.xlsx")

    # Read Excel file
    new_workbook = openpyxl.load_workbook("salary.xlsx")
    new_sheet = new_workbook.active

    return new_sheet.max_row - 1


# Extract first page of PDF
def extract_pdf_text(path: Union[str, Path]) -> str:
    document = fitz.open(path)
    text = document[0].get_text()
    document.close()
    return text[:100]


# Read JSON file with exception handling
def read_file(path: Union[str, Path]) -> Optional[dict]:
    try:
        with open(path, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        logger.error("File not found: %s", path)

    except json.JSONDecodeError:
        logger.error("Invalid JSON file: %s", path)

    return None


# Find employee by name
def find_employee(name: str) -> Optional[dict]:
    data = read_file("employees.json")

    if data is None:
        return None

    for employee in data["employees"]:
        if employee["name"].lower() == name.lower():
            return employee

    return None


# Main program
def main() -> None:

    # Read CSV
    employees = read_employees(Path("employees.csv"))

    # Write JSON
    write_json(employees)

    # Write high earners CSV
    count = write_high_earners(employees)

    print(
        f"Rows read: {len(employees)} | "
        f"High earners written: {count}"
    )

    # Create and read Excel
    rows = create_excel(employees)

    print(
        f"salary.xlsx created and read back: {rows} rows"
    )

    # Extract PDF text if sample.pdf exists
    pdf_path = Path("sample.pdf")

    if pdf_path.exists():
        pdf_text = extract_pdf_text(pdf_path)
        print("PDF first 100 characters:", pdf_text)

    # Demonstrate employee search
    employee = find_employee("Arun")

    # Demonstrate FileNotFoundError
    read_file("missing.txt")


if __name__ == "__main__":
    main()
