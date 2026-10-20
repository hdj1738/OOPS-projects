# Library Management System

## Overview

A command-line program for maintaining a book inventory and tracking whether each book is available or issued. It also defines student and researcher user types, but the current menu does not associate users with book loans.

## Workflow

The program starts in `2.py` and calls `load_books()`. If no records load, it prompts for an initial set of books and saves them. The menu can display all books, display available books, search by ID, issue an available book, or return an issued book. Successful issue and return operations save immediately; exit also saves.

## How to run

Requires Python 3 and uses only the Python standard library. From this directory, run:

```bash
python 2.py
```

Run from `library-management` because the data filename is resolved relative to the current working directory.

## Class structure

- `Book` stores a private book ID and availability state, plus author and title. `issue()` and `return_book()` change availability only when the operation is valid.
- `LibraryUser` is an abstract base class with abstract `get_role()`.
- `Person` inherits `LibraryUser` and stores name and person ID; it does not implement `get_role()`, so it remains abstract.
- `Student` and `Researcher` inherit `Person` and implement `get_role()`, returning their respective role strings. They also store course or research area.

## Implemented features

- List all books or only books marked available.
- Search for a book by ID.
- Issue available books and return issued books; reject unknown books, repeat issues, and returns of available books.
- Validate prompted values and reject duplicate IDs during initial entry.
- Handle a missing CSV file as an empty inventory; report missing header columns and skip malformed rows.

## Data persistence

The code uses Python's built-in `csv` module with `csv.DictReader` and `csv.DictWriter`. The only application data filename is `books.csv`, resolved in the current working directory. Its columns are `book_id`, `author`, `title`, and `availability`; availability is saved as `True` or `False`. The file is loaded at startup and rewritten after initial book entry, successful issue or return, and exit. No `books.csv` file was present in the project directory during this inspection.

**CSV-only audit:** Compliant in the inspected source and project files. The program imports no JSON module and uses no other persistent application data file.

## Limitations

- The menu does not create or use `Student` or `Researcher` records, so borrowers, loan dates, and return history are not tracked.
- If no valid records load, including when all rows are malformed, startup enters initial book setup; saving that setup replaces the CSV contents.
- The file uses the process's current working directory, so launching from another directory reads or creates a different `books.csv` there.

## Testing

No automated test files were found. An ad hoc persistence check was run during review and passed for a missing file, comma and quote handling in fields, issue/return state across reloads, and skipping a malformed row. The temporary test CSV was removed.

## Future improvements

- Add automated tests for CSV persistence, malformed records, and issue/return behavior.
- Link a borrower to each loan and store due and return dates if circulation history is required.
- Resolve the data path relative to the script if consistent file location across launch directories is desired.
