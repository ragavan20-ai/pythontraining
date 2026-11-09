
import csv

# Calculate bonus
def calculate_bonus(salary, rate=0.1, *extras, **options):
    bonus = salary * rate + sum(extras)

    if "cap" in options:
        bonus = min(bonus, options["cap"])

    return bonus


# Decorator
def log_call(func):
    def wrapper(*args, **kwargs):
        print("Calling get_details")
        return func(*args, **kwargs)
    return wrapper


# Employee class
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_details(self):
        return f"{self.name} - {self.salary}"

    @property
    def annual_salary(self):
        return self.salary * 12


# Manager class
class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    @log_call
    def get_details(self):
        return f"{self.name} - {self.salary} - Team Size: {self.team_size}"


# Read CSV file
with open("employees.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        name = row["name"]
        salary = int(row["salary"])

        if salary < 50000:
            print(name, "- Low Salary")
        elif salary < 70000:
            print(name, "- Medium Salary")
        else:
            print(name, "- High Salary")


# Create Manager object
manager = Manager("Divya", 75000, 5)

# Display manager details
print(manager.get_details())
