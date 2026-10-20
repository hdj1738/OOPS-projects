from abc import ABC, abstractmethod
import csv
def save_students(students):
    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["id", "name", "age", "course", "marks"])

        for student in students:
            marks = "|".join(
                f"{subject}:{mark}"
                for subject, mark in student.marks.items()
            )

            writer.writerow([
                student.id,
                student.name,
                student.age,
                student.course,
                marks
            ])
def load_students():
    students = []

    try:
        with open("students.csv", "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                marks = {}

                for item in row["marks"].split("|"):
                    subject, mark = item.split(":")
                    marks[subject] = int(mark)

                student = Student(
                    int(row["id"]),
                    row["name"],
                    int(row["age"]),
                    row["course"],
                    marks
                )

                students.append(student)

    except FileNotFoundError:
        print("No student file found. Starting with empty records.")

    return students

def main():
    students=load_students()
    while True:
        print("\n---- STUDENT MANAGEMENT MENU ----")
        print("1. Add students")
        print("2. Search student")
        print("3. Update student or marks")
        print("4. Delete student or mark")
        print("5. Display all students")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            n = get_valid_input("Enter number of students: ", int, positive=True)
            for _ in range(n):
                student_id = get_valid_input("Enter student id: ", int, positive=True)
                while any(student.id == student_id for student in students):
                    print("Duplicate student IDs are not allowed.")
                    student_id = get_valid_input("Enter student id: ", int, positive=True)
                age = get_valid_input("Enter student age: ", int, positive=True)
                name = get_valid_input("Enter student name: ", str)
                course = get_valid_input("Enter student course: ", str).lower()
                students.append(Student(student_id, name, age, course, get_valid_marks()))
            save_students(students)
        elif choice == "2":
            search_details(students)
        elif choice == "3":
            update_details(students)
            save_students(students)
        elif choice == "4":
            delete_details(students)
            save_students(students)
        elif choice == "5":
            for student in students:
                student.display_details()
        elif choice == "6":
            save_students(students)
            print("Exiting Student Management System.")
            return
        else:
            print("Invalid choice. Enter a number from 1 to 6.")

def search_details(students):
    found=False
    search = get_valid_input("Enter id that you want to search: ", int, positive=True)
    for student in students:
        if student.id==search:
            found=True
            student.display_details()
            break
    if not found:
        print("Student record with such id doesn't exist.") 

def update_details(students):
    found=False
    attribute_types = {"id": int,"name":str,"age":int,"course":str} 
    while True:
        changename = get_valid_input("Enter the attribute that you want to change: ", str).lower()
        if changename in attribute_types or changename == "marks":
            break
        print("Invalid attribute. Choose id, name, age, course, or marks.")
    changeid = get_valid_input("Enter the id of the student whose value you want to change: ", int , positive=True)
    if changename!="marks":
        newid = get_valid_input(f"Enter {changename} that you want to replace it with: ", attribute_types[changename])
        if changename == "id" and any(student.id == newid for student in students):
            print("Duplicate student IDs are not allowed.")
            return
        for student in students:
            if student.id==changeid:
                found=True
                setattr(student, changename,newid)
                break
        if not found:
            print("Student record with such id doesn't exist.")   
    else:
        for student in students:
            if student.id==changeid:
                found=True
                while True:
                    subject=get_valid_input("Enter subject:",str)
                    if subject in student.marks:
                        break
                    print("Cannot update subject that does not exist.")
                while True:
                    newmark=get_valid_input("Enter mark:",int)
                    if newmark>=0 and newmark<=100:
                        break
                    print("Number can only be between 0 and 100, 0 included.")
                
                student.marks[subject]=newmark
                break
        if not found:
            print("Student record with such id doesn't exist.")  

def delete_details(students):
    while True:
        found=False
        deletename = get_valid_input("Do you want to delete the student or mark: ", str).lower()
        if deletename=="student":
                deleteid = get_valid_input("Enter the id of the student whose value you want to delete: ", int , positive=True)
                for student in students:
                    if student.id==deleteid:
                        found=True
                        students.remove(student)
                        break
                if not found:
                    print("Student record with such id doesn't exist.")
                else:
                    break

        elif deletename=="mark":
            deleteid = get_valid_input("Enter the id of the student whose value you want to delete: ", int , positive=True)
            for student in students:
                if student.id==deleteid:
                    found=True
                    while True:
                        subject=get_valid_input("Enter the subject of the student whose mark you want to delete: ",str)
                        if subject in student.marks:
                            student.marks.pop(subject)
                            break
                        print("Cannot delete subject that does not exist.")
                    break
            if not found:
                print("Student record with such id doesn't exist.")
            else: 
                break
        else:
            print("Can only delete student or mark.")
    
    
    
             

def get_valid_input(prompt, value_type, positive=False):
    while True:
        try:
            value = value_type(input(prompt))

            if not value:
                print("Cannot be empty.")
                continue

            if positive and value <= 0:
                print("Value must be positive.")
                continue

            if "name" in prompt.lower() and (not any(char.isalpha() for char in value)
                    or any(not (char.isalpha() or char.isspace() or char in "-.'") for char in value)):
                print("Enter valid text using letters, spaces, apostrophes, or hyphens.")
                continue

            return value

        except ValueError:
            print("Invalid type. Try again.")
        

def get_valid_marks():
    while True:
        try:
            marks_input = input(
                "Enter student marks (e.g. Math,90 Python,85): "
            )

            if not marks_input.strip():
                print("Marks cannot be empty.")
                continue

            marks = marks_input.split()
            format_marks = {}

            for item in marks:
                subject, mark = item.split(",")
                mark = int(mark)

                if mark < 0 or mark > 100:
                    print("Marks must be between 0 and 100.")
                    break

                if not subject:
                    print("Subject cannot be empty.")
                    break

                format_marks[subject] = mark

            else:
                return format_marks

        except ValueError:
            print("Invalid format. Use Subject,Mark (e.g. Math,90).")

class StudentRecord(ABC):

    @abstractmethod
    def display_details(self):
        pass
    


class Student(StudentRecord):
    def __init__(self,id,name, age, course, marks):
        if not id or not name or id<=0 or not age or age<=0 or not course or not marks:
            raise ValueError("Cannot have null or invalid input")
        if (not any(char.isalpha() for char in name)
                or any(not (char.isalpha() or char.isspace() or char in "-.'") for char in name)):
            raise ValueError("Enter a valid student name.")
        self.id=id
        self.name=name
        self.age=age
        self.course=course
        self.marks=marks
     #whatshdastudentclassbeabletodo?
     #display student details
    def display_details(self):
        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Course: {self.course}")
        print(f"Marks: {self.marks}")
        print(f"Average: {self.calculate_average()}")
        print(f"Grade: {self.calculate_grade()}")
        highest_subject, highest_mark = self.highest_mark_subject()
        if highest_subject:
            print(f"Highest Mark Subject: {highest_subject}, Mark: {highest_mark}") 
        
        lowest_subject, lowest_mark = self.lowest_mark_subject()
        if lowest_subject:
            print(f"Lowest Mark Subject: {lowest_subject}, Mark: {lowest_mark}") 

    #watstudentshldowidmarks
    def calculate_average(self):
        total_marks = sum(self.marks.values())
        num_subjects = len(self.marks)
        average = total_marks / num_subjects if num_subjects > 0 else 0
        return average
    
    def calculate_grade(self):
        average = self.calculate_average()
        if average >= 90:
            return "S"
        elif average >= 80:
            return "A"
        elif average >= 70:
            return "B"
        elif average >= 60:
            return "C"
        elif average >= 50:
            return "D"
        else:
            return "F"

    def highest_mark_subject(self):
                if not self.marks:
                    return None, None
                highest_subjects=[]
                highest_mark=max(self.marks.values())
                for k in self.marks.keys():
                    if self.marks[k]==highest_mark:
                        highest_subjects.append(k)
                    
                return ",".join(highest_subjects),highest_mark

    def lowest_mark_subject(self):
            if not self.marks:
                return None, None
            lowest_subjects=[]
            lowest_mark=min(self.marks.values())
            for k in self.marks.keys():
                if self.marks[k]==lowest_mark:
                    lowest_subjects.append(k)
                
            return ",".join(lowest_subjects),lowest_mark
        
class Password():
    def __init__(self,pw):
        if not pw:
            raise ValueError("Cannot have null or invalid input")
        self.__pw=pw

    @property
    def pw(self):
        return self.__pw
    
    @pw.setter
    def pw(self,pswd):
        if not pswd:
            raise ValueError("Password cannot be empty.")
        self.__pw =pswd

    

if __name__=="__main__":        
    while True:
        pswd = get_valid_input("Enter password: ", str)
        password = Password(pswd)
        if password.pw == "hiralissocool":
            main()
            break
        print("Incorrect password.")

