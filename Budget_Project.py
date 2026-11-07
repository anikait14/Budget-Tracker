import csv
import os
from datetime import date
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

DATA_FILE = "budget_data.csv"
FIELDNAMES = ["date", "type", "category", "amount", "description"]


class BudgetTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Budget Tracker")
        self.root.geometry("1100x720")
        self.root.minsize(900, 600)

        self.transactions = []
        self.search_var = tk.StringVar()
        self.category_filter_var = tk.StringVar(value="All categories")
        self.editing_index = None

        self.create_file_if_missing()
        self.configure_styles()
        self.create_widgets()
        self.load_transactions()
        self.refresh_table()
        self.update_summary()

    def configure_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("App.TFrame", background="#f4f7fb")
        style.configure("Header.TFrame", background="#17324d")
        style.configure("Header.TLabel", background="#17324d", foreground="white")
        style.configure("HeaderTitle.TLabel", background="#17324d", foreground="white",
                        font=("Segoe UI", 24, "bold"))
        style.configure("HeaderSubtitle.TLabel", background="#17324d", foreground="#c8d8e8",
                        font=("Segoe UI", 10))
        style.configure("Card.TFrame", background="white", relief="solid", borderwidth=1)
        style.configure("CardLabel.TLabel", background="white", foreground="#68788a",
                        font=("Segoe UI", 10, "bold"))
        style.configure("CardValue.TLabel", background="white", foreground="#17324d",
                        font=("Segoe UI", 20, "bold"))
        style.configure("Section.TLabel", background="#f4f7fb", foreground="#17324d",
                        font=("Segoe UI", 12, "bold"))
        style.configure("Accent.TButton", background="#1d7a68", foreground="white",
                        font=("Segoe UI", 10, "bold"), padding=(14, 8))
        style.map("Accent.TButton", background=[("active", "#155d50")])
        style.configure("Treeview", background="white", fieldbackground="white",
                        foreground="#263746", rowheight=32, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#dce8f1", foreground="#17324d",
                        font=("Segoe UI", 10, "bold"), padding=8)
        style.map("Treeview", background=[("selected", "#b9dcd4")],
                  foreground=[("selected", "#17324d")])

    def create_file_if_missing(self):
        """Creates the CSV file with headers if it does not already exist."""
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
                writer.writeheader()

    def create_widgets(self):
        self.root.configure(bg="#f4f7fb")

        header = ttk.Frame(self.root, style="Header.TFrame", padding=(28, 22))
        header.pack(fill="x")
        ttk.Label(header, text="PERSONAL FINANCE", style="HeaderSubtitle.TLabel").pack(anchor="w")
        ttk.Label(header, text="Budget Dashboard", style="HeaderTitle.TLabel").pack(anchor="w", pady=(2, 0))
        ttk.Label(header, text="Track your money with clarity and confidence.",
                  style="HeaderSubtitle.TLabel").pack(anchor="w", pady=(3, 0))

        content = ttk.Frame(self.root, style="App.TFrame", padding=(24, 18))
        content.pack(fill="both", expand=True)

        cards = ttk.Frame(content, style="App.TFrame")
        cards.pack(fill="x", pady=(0, 18))
        self.income_value = self.create_card(cards, "TOTAL INCOME", "$0.00", 0)
        self.expense_value = self.create_card(cards, "TOTAL EXPENSES", "$0.00", 1)
        self.balance_value = self.create_card(cards, "CURRENT BALANCE", "$0.00", 2)
        self.count_value = self.create_card(cards, "TRANSACTIONS", "0", 3)

        ttk.Label(content, text="Add a transaction", style="Section.TLabel").pack(anchor="w", pady=(0, 7))
        input_frame = ttk.Frame(content, style="Card.TFrame", padding=14)
        input_frame.pack(fill="x", pady=(0, 16))

        ttk.Label(input_frame, text="Date:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, date.today().isoformat())

        ttk.Label(input_frame, text="Type:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.type_box = ttk.Combobox(input_frame, values=["Income", "Expense"], state="readonly", width=12)
        self.type_box.grid(row=0, column=3, padx=5, pady=5)
        self.type_box.set("Expense")

        ttk.Label(input_frame, text="Category:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.category_entry = ttk.Entry(input_frame, width=18)
        self.category_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(input_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(input_frame, width=15)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Description:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.description_entry = ttk.Entry(input_frame, width=45)
        self.description_entry.grid(row=1, column=3, columnspan=3, padx=5, pady=5, sticky="we")

        button_frame = ttk.Frame(content, style="App.TFrame", padding=(0, 0, 0, 10))
        button_frame.pack(fill="x")

        self.add_button = ttk.Button(button_frame, text="Add Transaction", style="Accent.TButton",
                         command=self.add_transaction)
        self.add_button.pack(side="left", padx=(0, 5))
        ttk.Button(button_frame, text="Edit Selected", command=self.edit_selected).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear Inputs", command=self.clear_inputs).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Export Excel", command=self.export_transactions).pack(side="left", padx=5)
        ttk.Label(button_frame, text="Search:").pack(side="right", padx=(10, 4))
        search_entry = ttk.Entry(button_frame, textvariable=self.search_var, width=25)
        search_entry.pack(side="right")
        self.search_var.trace_add("write", lambda *_: self.refresh_table())
        ttk.Label(button_frame, text="Category:").pack(side="right", padx=(10, 4))
        self.category_filter = ttk.Combobox(button_frame, textvariable=self.category_filter_var,
                            state="readonly", width=18)
        self.category_filter.pack(side="right")
        self.category_filter.bind("<<ComboboxSelected>>", lambda event: self.refresh_table())

        ttk.Label(content, text="Transaction history", style="Section.TLabel").pack(anchor="w", pady=(0, 7))
        table_frame = ttk.Frame(content, style="Card.TFrame", padding=8)
        table_frame.pack(fill="both", expand=True)
        columns = ("date", "type", "category", "amount", "description")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        self.tree.heading("date", text="Date")
        self.tree.heading("type", text="Type")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("description", text="Description")

        self.tree.column("date", width=100)
        self.tree.column("type", width=100)
        self.tree.column("category", width=140)
        self.tree.column("amount", width=100)
        self.tree.column("description", width=380)

        self.tree.tag_configure("income", foreground="#16705e")
        self.tree.tag_configure("expense", foreground="#b84b4b")
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.status_label = ttk.Label(self.root, text="Ready", anchor="w",
                                      background="#e5edf3", foreground="#526779",
                                      padding=(24, 7))
        self.status_label.pack(fill="x", side="bottom")

    def create_card(self, parent, label, value, column):
        parent.columnconfigure(column, weight=1)
        card = ttk.Frame(parent, style="Card.TFrame", padding=(16, 12))
        card.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 8, 0))
        ttk.Label(card, text=label, style="CardLabel.TLabel").pack(anchor="w")
        value_label = ttk.Label(card, text=value, style="CardValue.TLabel")
        value_label.pack(anchor="w", pady=(4, 0))
        return value_label

    def load_transactions(self):
        """Loads all transactions from the CSV file into the program."""
        self.transactions.clear()

        with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    row["amount"] = float(row["amount"])
                    self.transactions.append(row)
                except ValueError:
                    # Skips corrupted rows instead of crashing the app
                    continue

    def save_transactions(self):
        """Writes the current transaction list back to the CSV file."""
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

            for transaction in self.transactions:
                writer.writerow({
                    "date": transaction["date"],
                    "type": transaction["type"],
                    "category": transaction["category"],
                    "amount": f"{float(transaction['amount']):.2f}",
                    "description": transaction["description"]
                })

    def refresh_table(self):
        """Refreshes the visible table in the Tkinter window."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.refresh_category_filter()
        search_text = self.search_var.get().strip().lower()
        visible_count = 0
        for index, transaction in enumerate(self.transactions):
            searchable = " ".join(str(transaction[field]) for field in FIELDNAMES).lower()
            if search_text and search_text not in searchable:
                continue
            selected_category = self.category_filter_var.get()
            if selected_category != "All categories" and transaction["category"] != selected_category:
                continue
            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    transaction["date"],
                    transaction["type"],
                    transaction["category"],
                    f"${float(transaction['amount']):.2f}",
                    transaction["description"]
                ),
                tags=(transaction["type"].lower(),)
            )
            visible_count += 1
        self.status_label.configure(text=f"Showing {visible_count} of {len(self.transactions)} transactions")

    def refresh_category_filter(self):
        categories = sorted({transaction["category"] for transaction in self.transactions})
        values = ["All categories"] + categories
        self.category_filter.configure(values=values)
        if self.category_filter_var.get() not in values:
            self.category_filter_var.set("All categories")

    def add_transaction(self):
        transaction_date = self.date_entry.get().strip()
        transaction_type = self.type_box.get().strip()
        category = self.category_entry.get().strip()
        amount_text = self.amount_entry.get().strip()
        description = self.description_entry.get().strip()

        if not transaction_date or not transaction_type or not category or not amount_text:
            messagebox.showerror("Missing Information", "Please fill in date, type, category, and amount.")
            return

        try:
            date.fromisoformat(transaction_date)
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Information", "Use a valid date (YYYY-MM-DD) and positive amount.")
            return

        transaction = {
            "date": transaction_date,
            "type": transaction_type,
            "category": category,
            "amount": amount,
            "description": description
        }

        if self.editing_index is None:
            self.transactions.append(transaction)
            status = "Transaction added successfully"
        else:
            self.transactions[self.editing_index] = transaction
            status = "Transaction updated successfully"
            self.editing_index = None
            self.add_button.configure(text="Add Transaction")
        self.save_transactions()
        self.refresh_table()
        self.update_summary()
        self.clear_inputs(keep_date=True)

        self.status_label.configure(text=status)

    def edit_selected(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showerror("No Selection", "Please select a transaction to edit.")
            return

        self.editing_index = int(selected_item[0])
        transaction = self.transactions[self.editing_index]
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, transaction["date"])
        self.type_box.set(transaction["type"])
        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, transaction["category"])
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, transaction["amount"])
        self.description_entry.delete(0, tk.END)
        self.description_entry.insert(0, transaction["description"])
        self.add_button.configure(text="Save Changes")
        self.status_label.configure(text="Editing selected transaction")

    def delete_selected(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showerror("No Selection", "Please select a transaction to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected transaction?")
        if not confirm:
            return

        selected_index = int(selected_item[0])
        self.transactions.pop(selected_index)

        self.save_transactions()
        self.refresh_table()
        self.update_summary()
        self.status_label.configure(text="Transaction deleted")

    def clear_inputs(self, keep_date=False):
        self.editing_index = None
        self.add_button.configure(text="Add Transaction")
        if not keep_date:
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, date.today().isoformat())

        self.type_box.set("Expense")
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def export_transactions(self):
        if not self.transactions:
            messagebox.showinfo("Nothing to Export", "Add at least one transaction before exporting.")
            return

        destination = filedialog.asksaveasfilename(
            title="Export Transactions",
            defaultextension=".xlsx",
            filetypes=[("Excel workbook", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not destination:
            return

        if os.path.splitext(destination)[1].lower() == ".csv":
            with open(destination, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
                writer.writeheader()
                for transaction in self.transactions:
                    writer.writerow({
                        "date": transaction["date"],
                        "type": transaction["type"],
                        "category": transaction["category"],
                        "amount": f"{float(transaction['amount']):.2f}",
                        "description": transaction["description"]
                    })
        else:
            try:
                from openpyxl import Workbook
                from openpyxl.styles import Font, PatternFill
            except ModuleNotFoundError:
                messagebox.showerror(
                    "Excel Export Unavailable",
                    "Excel export requires openpyxl. Run:\n\n"
                    "python -m pip install openpyxl\n\n"
                    "Then restart the application."
                )
                return

            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Transactions"
            sheet.append(FIELDNAMES)

            for cell in sheet[1]:
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill("solid", fgColor="17324D")

            for transaction in self.transactions:
                transaction_date = date.fromisoformat(transaction["date"])
                sheet.append([
                    transaction_date,
                    transaction["type"],
                    transaction["category"],
                    float(transaction["amount"]),
                    transaction["description"]
                ])

            for cell in sheet["A"][1:]:
                cell.number_format = "yyyy-mm-dd"
            for cell in sheet["D"][1:]:
                cell.number_format = '$#,##0.00'

            widths = {"A": 15, "B": 14, "C": 18, "D": 15, "E": 42}
            for column, width in widths.items():
                sheet.column_dimensions[column].width = width
            sheet.freeze_panes = "A2"
            sheet.auto_filter.ref = sheet.dimensions
            workbook.save(destination)

        self.status_label.configure(text=f"Exported {len(self.transactions)} transactions")

    def update_summary(self):
        total_income = 0
        total_expenses = 0
        expenses_by_category = defaultdict(float)

        for transaction in self.transactions:
            amount = float(transaction["amount"])

            if transaction["type"] == "Income":
                total_income += amount
            else:
                total_expenses += amount
                expenses_by_category[transaction["category"]] += amount

        balance = total_income - total_expenses
        self.income_value.configure(text=f"${total_income:,.2f}")
        self.expense_value.configure(text=f"${total_expenses:,.2f}")
        self.balance_value.configure(text=f"${balance:,.2f}")
        self.balance_value.configure(foreground="#16705e" if balance >= 0 else "#b84b4b")
        self.count_value.configure(text=str(len(self.transactions)))


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()
