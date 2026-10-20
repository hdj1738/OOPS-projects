from abc import ABC, abstractmethod
import csv
class Employee(ABC):
    def __init__(self,name,employee_id,department,employee_type):
        self.name=name
        self.__employee_id=employee_id
        self.department=department
        self.employee_type=employee_type
    def __str__(self):
            return f"employee ID:{self.get_employeeid()} employee name:{self.name} department:{self.department} type:{self.employee_type}"
    
    def get_employeeid(self):
        return self.__employee_id
 
    @abstractmethod
    def calculate_salary(self):
        pass

    def calculate_net_salary(self):
         gross=self.calculate_salary()
         return gross-gross/10,gross/10,gross

class FullTimeEmployee(Employee):
    def __init__(self,name,employee_id,department,monthly_salary):
        super().__init__(name,employee_id,department,"fulltimeemployee")
        self.__monthly_salary=monthly_salary
    def calculate_salary(self):
         return self.__monthly_salary

class PartTimeEmployee(Employee):
    def __init__(self,name,employee_id,department,hours_worked,hourly_rate):
            super().__init__(name,employee_id,department,"parttimeemployee")
            self.__hours_worked=hours_worked
            self.__hourly_rate=hourly_rate
    def calculate_salary(self):
             return self.__hours_worked*self.__hourly_rate

def error_present(value):
    if type(value)==int or type(value)==float:
        if value<0:
            return True
    else:
        if value.strip()=="":
            return True
    return False
        
def looping_error_checking(prompt,datatype):
    while True:
        try:
            inputvalue=datatype(input(f"Enter {prompt}: "))
            if prompt in ["employee_id","account_number","hourly_rate","monthly_salary"]:
                if inputvalue==0:
                    raise ValueError("Zero not allowed.")
            if error_present(inputvalue):
                raise ValueError
            if prompt == "name" and (not any(char.isalpha() for char in inputvalue)
                    or any(not (char.isalpha() or char.isspace() or char in "-'.’") for char in inputvalue)):
                raise ValueError
            if prompt == "Number of employees" and inputvalue <= 0:
                raise ValueError
            if prompt == "hours_worked" and inputvalue <= 0:
                raise ValueError
            return inputvalue
        except ValueError:
            print(f"Invalid input.")
   
        
def main():
    employees=load_employees()
    if employees is None:
        print("Unable to load employee records. Fix employees.csv before restarting.")
        return

    if not employees:
        n=looping_error_checking("Number of employees",int)
        for i in range(n):
            name=looping_error_checking("name",str)
            while True:
                employee_id=looping_error_checking("employee_id",int)
                if not search(employees,employee_id):
                    break
                print("Duplicate Ids not allowed.")
            department=looping_error_checking("department",str)
            while True:
                employee_type=looping_error_checking("employee type (fulltimeemployee or parttimeemployee)",str).strip().lower()
                if employee_type == "fulltimeemployee":
                    monthly_salary=looping_error_checking("monthly_salary",float)
                    employee = FullTimeEmployee(name,employee_id,department,monthly_salary)
                    break
                elif employee_type == "parttimeemployee":
                    hours_worked=looping_error_checking("hours_worked",int)
                    hourly_rate=looping_error_checking("hourly_rate",float)
                    employee = PartTimeEmployee(name,employee_id,department,hours_worked,hourly_rate)
                    break
                else:
                    print("Invalid employee type.")
            employees.append(employee) 
        save_employees(employees)


    while True:
        print("\n---- EMPLOYEE PAYROLL MENU ----")
        print("1. Display all employees")
        print("2. Search employee")
        print("3. Calculate gross salary")
        print("4. Display salary slip")
        print("5. Add employee")
        print("6. Remove employee")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display(employees)

        elif choice == "2":
            employee_id = looping_error_checking("employee_id", int)
            result = display(employees, employee_id)
            if not result:
                print("Employee not found.")

        elif choice == "3":
            employee_id = looping_error_checking("employee_id", int)
            result = search(employees, employee_id)
            if result:
                print("Gross salary:", result.calculate_salary())
            else:
                print("Employee not found.")

        elif choice == "4":
            employee_id = looping_error_checking("employee_id", int)
            display_salary_slip(employees, employee_id)

        elif choice == "5":
            employee = get_employee_input(employees)
            employees.append(employee)
            save_employees(employees)

        elif choice == "6":
            employee_id = looping_error_checking("employee_id", int)
            employee = search(employees, employee_id)
            if employee:
                employees.remove(employee)
                save_employees(employees)
                print("Employee removed.")
            else:
                print("Employee not found.")

        elif choice == "7":
            save_employees(employees)
            print("Exiting Employee Payroll System.")
            break

        else:
            print("Invalid choice. Enter a number from 1 to 7.")


def get_employee_input(employees):
    name = looping_error_checking("name", str)
    while True:
        employee_id = looping_error_checking("employee_id", int)
        if not search(employees, employee_id):
            break
        print("Duplicate Ids not allowed.")
    department = looping_error_checking("department", str)
    while True:
        employee_type = looping_error_checking("employee type (fulltimeemployee or parttimeemployee)", str).strip().lower()
        if employee_type == "fulltimeemployee":
            return FullTimeEmployee(name, employee_id, department,
                                    looping_error_checking("monthly_salary", float))
        if employee_type == "parttimeemployee":
            hours = looping_error_checking("hours_worked", int)
            if hours <= 0:
                print("Invalid input.")
                continue
            rate = looping_error_checking("hourly_rate", float)
            return PartTimeEmployee(name, employee_id, department, hours, rate)
        print("Invalid employee type.")


def display(employees,id_to_search=False):
    if id_to_search is False:
        for employee in employees:
            print(employee)
    else:
        #id_to_search=looping_error_checking("id_to_search",int)
        res=search(employees,id_to_search)
        if res:
            print(res)
        else:
            return False
        return res

 
def display_salary_slip(employees, id_to_search):
    print("---- salary slip ----")
    res = display(employees, id_to_search)
    if res:
        netsal, deduct, gross = res.calculate_net_salary()
        print(f"Net salary: {netsal} deductions: {deduct} gross salary: {gross}")
    else:
        print("Employee not found.")
   

def search(employees,id_to_search):
    for employee in employees:
        if id_to_search==employee.get_employeeid():
                return employee
    return False
                

def save_employees(employees):
    fieldnames = ["name", "employee_id", "department", "employee_type",
                  "monthly_salary", "hours_worked", "hourly_rate"]
    with open("employees.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for employee in employees:
            item = {
                "name": employee.name,
                "employee_id": employee.get_employeeid(),
                "department": employee.department,
                "employee_type": employee.employee_type
            }
            if isinstance(employee, FullTimeEmployee):
                item["monthly_salary"] = employee._FullTimeEmployee__monthly_salary
            elif isinstance(employee, PartTimeEmployee):
                item["hours_worked"] = employee._PartTimeEmployee__hours_worked
                item["hourly_rate"] = employee._PartTimeEmployee__hourly_rate
            writer.writerow(item)
    print("Employee records saved successfully.")
          



def load_employees():
    try:
        with open("employees.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            required_fields = {"name", "employee_id", "department", "employee_type",
                               "monthly_salary", "hours_worked", "hourly_rate"}
            if (not reader.fieldnames or not required_fields.issubset(reader.fieldnames)
                    or len(reader.fieldnames) != len(required_fields)):
                print("Error loading employee records: missing CSV columns.")
                return None

            employees = []
            for row_number, item in enumerate(reader, start=2):
                try:
                    if (None in item or any(value is None for value in item.values())
                            or not item["name"].strip() or not item["department"].strip()):
                        raise ValueError("Incomplete employee record.")
                    if item["employee_type"] == "fulltimeemployee":
                        employee = FullTimeEmployee(
                            item["name"], int(item["employee_id"]), item["department"],
                            float(item["monthly_salary"])
                        )
                    elif item["employee_type"] == "parttimeemployee":
                        employee = PartTimeEmployee(
                            item["name"], int(item["employee_id"]), item["department"],
                            int(item["hours_worked"]), float(item["hourly_rate"])
                        )
                    else:
                        raise ValueError("Unknown employee type.")
                    if employee.get_employeeid() <= 0:
                        raise ValueError("Invalid employee values.")
                    if isinstance(employee, FullTimeEmployee) and employee.calculate_salary() <= 0:
                        raise ValueError("Invalid monthly salary.")
                    if isinstance(employee, PartTimeEmployee) and (
                            employee._PartTimeEmployee__hours_worked < 0
                            or employee._PartTimeEmployee__hourly_rate <= 0):
                        raise ValueError("Invalid part-time pay values.")
                    employees.append(employee)
                except (TypeError, ValueError):
                    print(f"Skipping malformed employee record on row {row_number}.")
            return employees
    except FileNotFoundError:
        return []
    except (OSError, csv.Error, UnicodeDecodeError):
        print("Error loading employee records.")
        return None


if __name__ == "__main__":
    main()

