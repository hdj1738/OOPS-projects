# Student Records System

## Overview

A command-line learning project for storing student details and subject marks, and displaying basic academic summaries.

## Workflow

When run directly, `1.py` prompts for a password and calls `main()` only when it matches the hard-coded value in the source. `main()` loads `students.csv`, prompts for a number of new students, collects each student's ID, age, name, course, and marks, then runs one search, one update, and a delete operation before saving all records. Student methods calculate average, grade, and highest and lowest marks.

## How to run

Requires Python 3 and uses only the Python standard library. From this directory, run:

```bash
python 1.py
```

Run from `student-records` because `students.csv` is opened relative to the current working directory. The inspected folder includes a sample `students.csv`.

## Class structure

- `StudentRecord` is an abstract base class with abstract `display_details()`.
- `Student` inherits `StudentRecord`, implements `display_details()`, stores student fields and marks, and provides average, grade, and highest/lowest subject calculations.
- `Password` stores a private password with a property getter and setter that reject empty values.

## Implemented features

- Read and write student data using Python's built-in CSV module.
- Add student records and search by ID.
- Update a student's ID, name, age, course, or an existing subject mark.
- Delete a student record or one of that student's marks.
- Validate prompted input and require entered marks to be between 0 and 100.
- Calculate average marks, grade bands, and highest and lowest marks (including tied subjects).

## Data persistence

The code reads and writes `students.csv` in the current working directory using `csv.DictReader` and `csv.writer`. The header fields are `id`, `name`, `age`, `course`, and `marks`. Marks are stored in one cell as subject and integer pairs separated by `|`, with each pair written as `subject:mark` (for example, `Math:90|Python:85`). The sample file contains four records. Records load at startup; the complete list is saved after the search, update, and delete steps finish.

**CSV-only audit:** Compliant in the inspected source and project files. No JSON imports or other persistent application data formats were found.

## Limitations

- Startup always asks for a positive number of new students, even when records already exist.
- The workflow performs one search, one update, and one delete before saving; it is not a repeating menu.
- The password is hard-coded in the source and is not secure authentication.
- `load_students()` only handles a missing file. Malformed rows or invalid mark encodings can raise errors.
- The code does not reject duplicate student IDs.
- Marks are manually encoded inside a CSV field, and subjects containing `|` or `:` are not supported by that encoding.
- If no file exists, the program starts with no records, but the `Student` constructor requires a non-empty marks dictionary.

## Testing

No automated test files were found in this project, and no tests were run as part of this documentation update.

## Future improvements

- Add automated tests for record operations, calculations, and valid and malformed CSV input.
- Add a repeating menu and avoid forcing a new-student count on every run.
- Reject duplicate IDs and handle malformed CSV rows without stopping the program.
- Replace the hard-coded password with an appropriate authentication mechanism if access control is needed.
