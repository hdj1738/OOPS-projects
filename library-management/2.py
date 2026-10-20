from abc import ABC, abstractmethod
import csv
class Book:
    def __init__ (self,book_id, author, title):
        if error_present(book_id) or error_present(author) or error_present(title):
            raise ValueError("Book ID must be positive and name of author and book cannot be empty.")
        self.__book_id=book_id
        self.author=author
        self.title=title
        self.__availability=True

    def __str__(self):
        return f"{self.get_book_id()} - {self.title} by {self.author}"
    #getter
    def get_book_id(self):
        return self.__book_id
    #now to check availability
    def is_available(self):
        return self.__availability

    def issue(self):
        if self.is_available():
            self.__availability=False
            return True
        return False
    def return_book(self):
        if not self.is_available():
            self.__availability=True
            return True
        return False
class LibraryUser(ABC):
    @abstractmethod
    def get_role(self):
        pass

class Person(LibraryUser):
    def __init__(self,name,person_id):
        self.name=name
        self.person_id=person_id

class Student(Person):
    def __init__(self,name, person_id,course):
        super().__init__(name,person_id)
        self.course=course
    def get_role(self):
        return "student"

class Researcher(Person):
    def __init__(self,name, person_id,research_area):
        super().__init__(name,person_id)
        self.research_area=research_area
    def get_role(self):
        return "researcher"
    
def error_present(value):
    if type(value)==int:
        if value<=0:
            return True
    else:
        if value.strip()=="":
            return True
    return False
        
def looping_error_checking(prompt,datatype):
    while True:
        try:
            inputvalue=datatype(input(f"Enter {prompt}: "))
            if error_present(inputvalue):
                raise ValueError
            return inputvalue
        except ValueError:
            print(f"Invalid input.")
              
def main():
    books=load_books()
    if books is None:
        print("Unable to load book records. Fix books.csv before restarting.")
        return
    if not books:
        n=looping_error_checking("Number of books",int)
        
        for i in range(n):
                while True:
                    book_id=looping_error_checking("book id",int)
                    if not search(books,book_id):
                        break
                    print("Duplicate Ids not allowed.")
                author=looping_error_checking("author",str)
                title=looping_error_checking("title",str)
                book=Book(book_id,author,title)
                books.append(book)
        save_books(books)

    print("---- menu ----")

    while True:
        print("1. Display all books")
        print("2. Display available books")
        print("3. Search for a book")
        print("4. Issue a book")
        print("5. Return a book")
        print("6. Add a book")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            display(books, "all")
        elif choice == "2":
            display(books, "available")
        elif choice == "3":
            display(books, "specific")
        elif choice == "4":
            issue_books(books)
        elif choice == "5":
            return_books(books)
        elif choice == "6":
            book_id = looping_error_checking("book id", int)
            while search(books, book_id):
                print("Duplicate Ids not allowed.")
                book_id = looping_error_checking("book id", int)
            author = looping_error_checking("author", str)
            title = looping_error_checking("title", str)
            books.append(Book(book_id, author, title))
            save_books(books)
        elif choice == "7":
            save_books(books)
            print("Exiting Library Management System.")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 7.")


def search(books,book_id_to_search=None):
    if book_id_to_search is None:
        book_id_to_search=looping_error_checking("book_id_to_search",int)
    for book in books:
        if book.get_book_id()==book_id_to_search:
            return book
    return None

def display(books,mode="all"):
    found=False
    if mode=="specific":
        book_id_details_to_display=looping_error_checking("book_id_details_to_display",int)
        result=search(books,book_id_details_to_display)
        if result:
            print(result)
            found=True
        else:
            print("Book_id does not exist.")
    elif mode=="available":
        for book in books:
            if book.is_available():
                print(book)
                found=True
    elif mode=="all":
        for book in books:
            print(book)
        found=True
    else:
        print("incorrect/invalid mode.")
    if not found:
        print("No matching books found.")

def issue_books(books):
    book_issueid=looping_error_checking("book_issueid",int) 
    result=search(books,book_issueid)
    if result:
        if result.issue():
            save_books(books)
            print("Book successfully issued.")
        else:
            print("Book already issued.")
    else:
        print("Book not available to issue.")


def return_books(books):
    book_returnid=looping_error_checking("book_returnid",int) 
    result=search(books,book_returnid)
    if result:
        if not result.is_available(): 
            result.return_book()
            save_books(books)
            print("Book successfully returned.")
        else:
            print("Book not issued and so cannot return")
    else:
        print("Book not availabe to return.")



def save_books(books):
    with open("books.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["book_id", "author", "title", "availability"]
        )
        writer.writeheader()
        for book in books:
            writer.writerow({
                "book_id": book.get_book_id(),
                "author": book.author,
                "title": book.title,
                "availability": book.is_available()
            })
    print("Books saved successfully.")

def load_books():
    try:
        with open("books.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            required_fields = {"book_id", "author", "title", "availability"}
            if not reader.fieldnames or not required_fields.issubset(reader.fieldnames):
                print("Error loading book records: missing CSV columns.")
                return None

            books = []
            for row_number, item in enumerate(reader, start=2):
                try:
                    book_id = int(item["book_id"])
                    availability = item["availability"].strip().lower()
                    if availability not in {"true", "false"}:
                        raise ValueError("invalid availability")
                    book = Book(book_id, item["author"], item["title"])
                    if availability == "false":
                        book.issue()
                    books.append(book)
                except (AttributeError, TypeError, ValueError):
                    print(f"Skipping malformed book record on row {row_number}.")
        return books
    except FileNotFoundError:
        return []
    except (OSError, csv.Error, UnicodeDecodeError):
        print("Error loading book records.")
        return None
if __name__ == "__main__":
    main()
