# Bank Account Management System

## Overview

A command-line learning project for maintaining customer records and savings or current accounts. It demonstrates account-specific withdrawal rules and basic account operations. It is not suitable for real banking or sensitive customer data.

## Workflow

The program starts in `3.py` and calls `load_accounts()`. If `bank_accounts.csv` is missing, it prompts for customer and account information and saves the resulting accounts. A CSV file with missing columns or an unreadable file is reported and startup stops so it is not overwritten. Malformed rows are reported and skipped; any valid rows remain available. The menu supports listing accounts, searching by account number, checking balances, depositing, withdrawing, viewing transaction history, and calculating savings interest. Successful deposits and withdrawals are saved immediately; the program also saves on exit.

## How to run

Requires Python 3 and uses only the Python standard library. From this directory, run:

```bash
python 3.py
```

Run from `bank-management` because the data filename is resolved relative to the current working directory.

## Class structure

- `Customer` stores a name, private customer ID, and phone number; `get_customerid()` exposes the ID.
- `Bank_Account` is an abstract base class with private account number and balance, shared deposit/withdrawal and transaction-history methods, and abstract `can_withdraw()`.
- `Savings_Account` inherits `Bank_Account` and overrides `can_withdraw()` to require a positive withdrawal within the balance. It also calculates simple interest.
- `Current_Account` inherits `Bank_Account` and overrides `can_withdraw()` to allow a positive withdrawal within balance plus overdraft limit.

## Implemented features

- Create savings and current accounts and reject duplicate customer IDs and account numbers during initial entry.
- Display accounts and search by account number.
- Check balances, deposit funds, and apply account-specific withdrawal rules.
- Keep deposit and withdrawal descriptions in transaction history and display that history.
- Calculate simple savings interest using `rate times balance times years / 100`.
- Validate prompted values, including a 10-digit phone number.

## Data persistence

The code uses Python's built-in `csv` module and reads and writes `bank_accounts.csv` in the current working directory. The columns are `name`, `customer_id`, `phone_number`, `account_number`, `balance`, `account_type`, `transaction_history`, `interest_rate`, and `overdraft_limit`. The unused account-type-specific column is blank. IDs are restored as integers; balances, rates, and limits as floats. Transaction history is stored in one field as an inner CSV row, preserving commas, quotes, and newlines in individual entries. A missing file starts with an empty account list. Malformed rows are reported and skipped; valid rows are retained.

**CSV-only audit:** Compliant in the current source. The application uses only `bank_accounts.csv` for persistent data. Existing `bank_accounts.json` data is not imported automatically.

## Limitations

- Transaction descriptions have no timestamps or transaction IDs.
- Interest is a simple calculation and is not added to the balance.
- Account data and transaction history are stored locally in CSV; validation is primarily performed at interactive prompts.
- No account or customer editing, deletion, or separate customer-listing menu is provided.

## Testing

No automated test files are included. An ad hoc assertion-based check passed for loading a missing file, saving and reloading both account types, preserving CSV-special characters and transaction history, account operations, interest, overdraft rules, and skipping a malformed row while retaining valid rows. This check was run during implementation and is not included as a project test file.

## Future improvements

- Add tests for account loading, saving, deposits, withdrawals, overdrafts, and interest calculations.
- Add transaction timestamps and clearer error reporting for invalid records.
