# Personal Budget Tracker

A desktop personal finance application built with **Python** and **Tkinter** to help users record income and expenses, monitor their balance, and manage their transaction history in one place. Transactions are saved locally to a CSV file, so data remains available between sessions.

## Features

- **Financial dashboard:** View total income, total expenses, current balance, and the number of recorded transactions.
- **Transaction management:** Add, edit, and delete income or expense entries with a date, category, amount, and optional description.
- **Search and filtering:** Search transaction details and filter the history by category.
- **Local data persistence:** Automatically load and save transactions using a CSV file.
- **Data export:** Export recorded transactions to `.csv` or formatted Excel (`.xlsx`) files.
- **Input validation:** Check for valid dates (`YYYY-MM-DD`), required fields, and positive transaction amounts.
- **Desktop interface:** Navigate transactions through a Tkinter table with a scroll bar and color-coded income and expense entries.

## Preview

_Add a screenshot of the application here to show the dashboard and transaction table._

<!-- After adding an image to your repository, you can use:
![Personal Budget Tracker dashboard](assets/dashboard.png)
-->

## Tech Stack

| Technology | Purpose |
| --- | --- |
| Python | Application logic and transaction processing |
| Tkinter / ttk | Desktop graphical user interface |
| CSV (Python standard library) | Local transaction storage and CSV export |
| `datetime`, `os`, `collections` | Date validation, file handling, and application utilities |
| openpyxl *(optional)* | Excel (`.xlsx`) export |

## Getting Started

### Prerequisites

- Python 3 installed, with Tkinter available.
- `openpyxl` is only needed if you want to export Excel workbooks. The application can run and export CSV files without it.

> Tkinter is commonly included with Python installations on Windows and macOS. Some Linux distributions require a separate Tkinter package (for example, `python3-tk` on Ubuntu/Debian).

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
   ```

2. Open the project folder:

   ```bash
   cd YOUR-REPOSITORY
   ```

3. (Optional) Install the dependency required for Excel export:

   ```bash
   python -m pip install openpyxl
   ```

4. Run the application from the project directory:

   ```bash
   python "Budget_Project (1).py"
   ```

   If you rename the script, update the command accordingly. On some systems, use `python3` instead of `python`.

> **Before publishing:** Replace `YOUR-USERNAME` and `YOUR-REPOSITORY` with your GitHub details. The run command above matches the uploaded filename.

## How to Use

### Add a transaction

1. Enter a date in `YYYY-MM-DD` format (the current date is filled in automatically).
2. Choose **Income** or **Expense**.
3. Enter a category, a positive amount, and an optional description.
4. Click **Add Transaction**.

The transaction appears in the history table, and the dashboard totals update automatically.

### Edit or delete a transaction

- **Edit:** Select a row, click **Edit Selected**, modify the fields, and click **Save Changes**.
- **Delete:** Select a row, click **Delete Selected**, and confirm the deletion.
- **Clear Inputs:** Reset the entry form without adding a transaction.

### Search and filter

- Type in the **Search** field to find matching text across transaction details.
- Select an option in the **Category** dropdown to show only transactions in that category.

The dashboard totals represent all stored transactions, even when the table is filtered.

### Export transactions

Click **Export Excel** and choose a destination and file format:

- **Excel (`.xlsx`):** Creates a formatted workbook with column headers, date and currency formatting, an autofilter, and a frozen header row. Requires `openpyxl`.
- **CSV (`.csv`):** Exports the transaction records without additional dependencies.

Exports include all saved transactions, not only the rows currently visible after searching or filtering.

## Data Storage

The application creates `budget_data.csv` in the **current working directory** if it does not exist. This file stores transaction data using the following columns:

```csv
date,type,category,amount,description
2026-11-07,Income,Salary,1200.00,Part-time work
2026-11-07,Expense,Groceries,45.50,Weekly shopping
```

This example is illustrative; the app starts with an empty CSV if no data file exists.

**Privacy note:** Data is stored locally in plain-text CSV format. Avoid committing your personal `budget_data.csv` to a public repository. Consider adding it to `.gitignore`.

## Project Structure

```text
personal-budget-tracker/
├── Budget_Project (1).py   # Desktop application and business logic
├── README.md               # Project documentation
└── budget_data.csv         # Automatically generated at runtime
```

The application script includes the graphical interface, transaction validation, file storage, search/filter logic, summary calculations, and export functionality.

## Implementation Highlights

- Uses a `BudgetTrackerApp` class to organize UI setup and application behavior.
- Stores transaction records in memory and synchronizes additions, edits, and deletions with the local CSV file.
- Updates financial summaries after transaction changes.
- Connects Tkinter input controls to a searchable and filterable `ttk.Treeview` transaction table.
- Uses a file-save dialog and `openpyxl` to support formatted Excel exports.

## Possible Future Improvements

- Add monthly spending trends and category breakdown charts.
- Support customizable budgets and spending alerts.
- Add automated tests for transaction validation and summary calculations.
- Allow users to choose a data-storage location and import existing transactions.
- Package the application as a standalone desktop executable.

## Notes

- This is a **local desktop application**, not a website; it runs on a computer with Python and Tkinter installed.
- Monetary values are displayed with a `$` symbol; the application does not currently support multiple currencies.
- The CSV file is local storage, not an encrypted database or cloud backup.
