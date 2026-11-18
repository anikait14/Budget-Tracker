
# Personal Budget Tracker

A Python desktop application for managing personal finances through a graphical user interface built with Tkinter. Users can track income, expenses, and account balances, manage transactions, and organize financial records. Data is stored locally in a **CSV file**, allowing transactions to persist between application sessions without requiring a database.

## Setup

Clone the repository and navigate to the project directory:

```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

Install the optional dependency required for Excel export:

```bash
python -m pip install openpyxl
```

Run the application:

```bash
python "Budget_Project (1).py"
```

The application opens in a Tkinter desktop window. Python with Tkinter support is required.

## Desktop UI

The application provides a graphical dashboard for tracking and managing financial transactions.

| **Component** | **Description** |
| ------------- | --------------- |
| Dashboard | Displays total income, expenses, current balance, and transaction count |
| Add Transaction | Records new income or expense transactions |
| Edit Transaction | Updates existing transaction details |
| Delete Transaction | Removes selected transactions |
| Search | Searches transaction records |
| Category Filter | Displays transactions belonging to a selected category |
| Transaction History | Displays all recorded transactions in a table |
| Export | Exports financial records to CSV or Excel files |

The interface uses Tkinter and ttk widgets with a customized layout, styled buttons, and color-coded transaction information.

## Transaction Data

Each transaction contains the following fields:

| **Field** | **Description** |
| --------- | --------------- |
| Date | Transaction date in YYYY-MM-DD format |
| Type | Income or Expense |
| Category | User-defined transaction category |
| Amount | Positive numerical value |
| Description | Optional transaction details |

## Features

### Transaction Management

The application supports creating, viewing, updating, and deleting financial transactions.

- Add income and expense records.
- Edit or delete existing transactions.
- Validate dates and transaction amounts.
- Search transactions and filter records by category.

### Financial Dashboard

The dashboard automatically calculates and displays:

- Total income
- Total expenses
- Current balance (income minus expenses)
- Total number of transactions

Dashboard values update when transactions are added, edited, or deleted.

### Data Storage

Transactions are stored locally in `budget_data.csv` using Python's built-in CSV module.

- The CSV file is automatically created if it does not exist.
- Transactions are loaded when the application starts.
- Changes are saved automatically after transactions are added, updated, or deleted.
- Data persists between application sessions.

### Data Export

Users can export their transaction history into:

- **CSV (.csv):** For storing and sharing transaction records.
- **Excel (.xlsx):** For viewing formatted financial data in spreadsheet applications.

Excel export uses the OpenPyXL library and includes formatted headers, date and currency formatting, column sizing, and filtering.

## Tech Stack

| **Technology** | **Purpose** |
| -------------- | ----------- |
| Python | Application logic and data processing |
| Tkinter / ttk | Graphical user interface |
| CSV | Local transaction storage |
| OpenPyXL | Excel file generation and formatting |
| datetime | Date handling and validation |
| collections | Financial data organization |

## Project Structure

```text
Personal-Budget-Tracker/
│
├── Budget_Project (1).py    # Main application
├── README.md                # Project documentation
└── budget_data.csv          # Automatically generated transaction data
```

The application generates `budget_data.csv` when first launched.

## Usage

1. Launch the application using the setup instructions.
2. Enter the transaction date, type, category, amount, and optional description.
3. Click **Add Transaction** to save the record.
4. View updated financial totals on the dashboard.
5. Select a transaction to edit or delete it.
6. Use the search field or category filter to find specific transactions.
7. Click **Export Excel** to save transaction records as an Excel or CSV file.

## Future Improvements

- Add financial charts and spending visualizations.
- Implement monthly budgets and spending limits.
- Introduce recurring income and expense transactions.
- Add advanced reporting and date-based filtering.
- Integrate a database for more scalable data management.
