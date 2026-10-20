# Employee Payroll Management System

## Overview

A command-line learning project for storing employee records and calculating basic gross and net pay for full-time and part-time employees. The salary slip uses a fixed 10% deduction; this is not a tax-compliant payroll system.

## Workflow

The program starts in `4.py` and calls `load_employees()`. If `employees.csv` is missing, it prompts for employee details and pay information based on employee type, then saves the records. A CSV file with missing columns or an unreadable file is reported and startup stops so it is not overwritten. Malformed rows are reported and skipped; any valid rows remain available. The menu can list employees, search by ID, calculate gross salary, or display a salary slip. The program saves on initial entry and on exit; the menu does not change employee records.

## How to run

Requires Python 3 and uses only the Python standard library. From this directory, run:

```bash
python 4.py
```

Run from `employee-payroll` because the data filename is resolved relative to the current working directory.

## Class structure

- `Employee` is an abstract base class containing shared employee data, a private employee ID, `calculate_net_salary()`, and abstract `calculate_salary()`.
- `FullTimeEmployee` inherits `Employee` and overrides `calculate_salary()` to return its monthly salary.
- `PartTimeEmployee` inherits `Employee` and overrides `calculate_salary()` to return hours worked multiplied by hourly rate.

## Implemented features

- Create full-time and part-time employee records, checking for duplicate IDs during initial entry.
- Display employees and search by employee ID.
- Calculate gross salary according to employee type.
- Display a salary slip with gross pay, fixed 10% deduction, and net pay.
- Validate interactive values for type, emptiness, and configured nonnegative or nonzero rules.

## Data persistence

The code uses Python's built-in `csv` module and reads and writes `employees.csv` in the current working directory. Its columns are `name`, `employee_id`, `department`, `employee_type`, `monthly_salary`, `hours_worked`, and `hourly_rate`. The unused employee-type-specific columns are blank. Employee IDs and hours are restored as integers; salary and hourly rate are restored as floats. A missing file starts with an empty employee list. Malformed rows are reported and skipped; valid rows are retained.

**CSV-only audit:** Compliant in the current source. The application uses only `employees.csv` for persistent data. Existing `employees.json` data is not imported automatically.

## Limitations

- The 10% deduction is fixed and is not based on tax or payroll rules.
- The program has no employee editing or deletion, pay-period handling, attendance, or leave calculations.
- The save function reads subclass private values through name-mangled attribute names.
- Validation is performed at prompts rather than consistently in the model classes.

## Testing

No automated test files are included. An ad hoc assertion-based check passed for loading a missing file, saving and reloading both employee types, preserving CSV-special characters, gross/net salary calculations, salary-slip output, and skipping a malformed row while retaining valid rows. This check was run during implementation and is not included as a project test file.

## Future improvements

- Add tests for subclass salary calculations, deductions, and persistence.
- Make deduction rules configurable and represent pay periods explicitly.
