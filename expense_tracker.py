"""
Personal Expense and Budget Tracker - Core Logic
Handles data storage, validation, transactions, budget tracking, and reports.
"""

import json
import os
from datetime import datetime

DATA_FILE = "data.json"

DEFAULT_DATA = {
    "transactions": [],
    "monthly_budgets": {}
}

DEFAULT_INCOME_CATEGORIES = [
    "Salary",
    "Freelance",
    "Investments",
    "Gift",
    "Other"
]

DEFAULT_EXPENSE_CATEGORIES = [
    "Groceries",
    "Rent/Mortgage",
    "Utilities",
    "Transportation",
    "Healthcare",
    "Entertainment",
    "Dining Out",
    "Education",
    "Other"
]


# ==========================================
# STAGE 1: STORAGE & PERSISTENCE
# ==========================================

def load_data(file_path=DATA_FILE):
    """
    Loads financial data from a JSON file.
    Returns default data structure if file doesn't exist, is empty, or is corrupted.
    """
    if not os.path.exists(file_path):
        return {
            "transactions": [],
            "monthly_budgets": {}
        }

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return {"transactions": [], "monthly_budgets": {}}
            data = json.loads(content)
            if not isinstance(data, dict):
                return {"transactions": [], "monthly_budgets": {}}
            if "transactions" not in data or not isinstance(data["transactions"], list):
                data["transactions"] = []
            if "monthly_budgets" not in data or not isinstance(data["monthly_budgets"], dict):
                data["monthly_budgets"] = {}
            return data
    except (json.JSONDecodeError, IOError) as error:
        print(f"\n[Warning] Could not read '{file_path}' ({error}). Initializing fresh data.")
        return {"transactions": [], "monthly_budgets": {}}


def save_data(data, file_path=DATA_FILE):
    """
    Saves financial data to a JSON file with readable formatting.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        return True
    except IOError as error:
        print(f"\n[Error] Failed to save data to '{file_path}': {error}")
        return False


# ==========================================
# STAGE 2: VALIDATION HELPERS
# ==========================================

def get_valid_amount(prompt_text):
    """
    Prompts user for an amount and validates that it is a positive number.
    Re-prompts until valid input is given.
    """
    while True:
        user_input = input(prompt_text).strip()
        if not user_input:
            print("  [Error] Amount cannot be empty. Please enter a valid number.")
            continue
        # Remove currency symbol if user typed it
        clean_input = user_input.lstrip("$£€")
        try:
            amount = float(clean_input)
            if amount <= 0:
                print("  [Error] Amount must be greater than zero.")
                continue
            return round(amount, 2)
        except ValueError:
            print("  [Error] Invalid amount. Please enter a valid positive number (e.g. 25.50).")


def get_valid_date(prompt_text, default_to_today=True):
    """
    Prompts user for a date in YYYY-MM-DD format.
    Optionally defaults to today's date if left blank.
    """
    today_str = datetime.today().strftime("%Y-%m-%d")
    while True:
        display_prompt = f"{prompt_text} (default: {today_str}): " if default_to_today else f"{prompt_text}: "
        user_input = input(display_prompt).strip()
        if not user_input and default_to_today:
            return today_str

        try:
            parsed_date = datetime.strptime(user_input, "%Y-%m-%d")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            print("  [Error] Invalid date format. Please use YYYY-MM-DD (e.g., 2026-11-19).")


def get_valid_month(prompt_text, default_to_current=True):
    """
    Prompts user for a month in YYYY-MM format.
    """
    current_month = datetime.today().strftime("%Y-%m")
    while True:
        display_prompt = f"{prompt_text} (default: {current_month}): " if default_to_current else f"{prompt_text}: "
        user_input = input(display_prompt).strip()
        if not user_input and default_to_current:
            return current_month

        try:
            parsed_month = datetime.strptime(user_input, "%Y-%m")
            return parsed_month.strftime("%Y-%m")
        except ValueError:
            print("  [Error] Invalid month format. Please use YYYY-MM (e.g., 2026-11).")


def get_valid_category(categories_list):
    """
    Displays categorized options and allows selecting by number or entering a custom category.
    """
    print("\nSelect a category:")
    for idx, category in enumerate(categories_list, start=1):
        print(f"  {idx}. {category}")
    print(f"  {len(categories_list) + 1}. [Custom Category]")

    while True:
        choice = input(f"Choose category (1-{len(categories_list) + 1}): ").strip()
        if not choice.isdigit():
            print("  [Error] Please enter a valid number.")
            continue
        choice_idx = int(choice)
        if 1 <= choice_idx <= len(categories_list):
            return categories_list[choice_idx - 1]
        elif choice_idx == len(categories_list) + 1:
            while True:
                custom = input("Enter custom category name: ").strip()
                if custom:
                    return custom.title()
                print("  [Error] Category name cannot be empty.")
        else:
            print(f"  [Error] Choice out of range. Enter 1-{len(categories_list) + 1}.")


def get_non_empty_string(prompt_text, default_value=""):
    """
    Prompts user for text, ensuring it is not empty.
    """
    while True:
        user_input = input(prompt_text).strip()
        if not user_input and default_value:
            return default_value
        if user_input:
            return user_input
        print("  [Error] Input cannot be blank.")


def generate_next_id(transactions):
    """
    Finds the maximum ID in existing transactions and returns next integer ID.
    """
    if not transactions:
        return 1
    return max(t.get("id", 0) for t in transactions) + 1


# ==========================================
# STAGE 2: RECORDING TRANSACTIONS
# ==========================================

def add_income(data, file_path=DATA_FILE):
    """
    Prompts for income details, validates inputs, records the transaction, and saves data.
    """
    print("\n--- [Add Income] ---")
    amount = get_valid_amount("Enter income amount ($): ")
    category = get_valid_category(DEFAULT_INCOME_CATEGORIES)
    date = get_valid_date("Enter date (YYYY-MM-DD)")
    description = get_non_empty_string("Enter description (e.g., Monthly paycheck): ")

    new_id = generate_next_id(data["transactions"])
    transaction = {
        "id": new_id,
        "type": "income",
        "amount": amount,
        "category": category,
        "date": date,
        "description": description
    }

    data["transactions"].append(transaction)
    if save_data(data, file_path):
        print(f"\n✓ Successfully recorded income of ${amount:,.2f} under '{category}'. (ID: {new_id})")
    return transaction


def add_expense(data, file_path=DATA_FILE):
    """
    Prompts for expense details, validates inputs, records transaction, saves data,
    and checks if monthly budget is exceeded.
    """
    print("\n--- [Record Expense] ---")
    amount = get_valid_amount("Enter expense amount ($): ")
    category = get_valid_category(DEFAULT_EXPENSE_CATEGORIES)
    date = get_valid_date("Enter date (YYYY-MM-DD)")
    description = get_non_empty_string("Enter description (e.g., Grocery shopping): ")

    new_id = generate_next_id(data["transactions"])
    transaction = {
        "id": new_id,
        "type": "expense",
        "amount": amount,
        "category": category,
        "date": date,
        "description": description
    }

    data["transactions"].append(transaction)
    if save_data(data, file_path):
        print(f"\n✓ Successfully recorded expense of ${amount:,.2f} under '{category}'. (ID: {new_id})")

    # Check budget warning for the month of this expense
    expense_month = date[:7]
    check_budget_warning(data, expense_month)

    return transaction


# ==========================================
# STAGE 3: HISTORY & FINANCIAL CALCULATIONS
# ==========================================

def view_transactions(data):
    """
    Displays formatted transaction history.
    """
    transactions = data.get("transactions", [])
    if not transactions:
        print("\nNo transactions recorded yet.")
        return

    print("\n" + "=" * 80)
    print(f"{'ID':<5} | {'Date':<10} | {'Type':<8} | {'Category':<16} | {'Amount ($)':<12} | {'Description'}")
    print("-" * 80)

    for item in transactions:
        t_id = item.get("id", "-")
        date = item.get("date", "-")
        t_type = item.get("type", "-").capitalize()
        category = item.get("category", "-")[:16]
        amount = item.get("amount", 0.0)
        desc = item.get("description", "-")

        # Color-like indicators with +/-
        amount_str = f"+${amount:,.2f}" if item.get("type") == "income" else f"-${amount:,.2f}"
        print(f"{t_id:<5} | {date:<10} | {t_type:<8} | {category:<16} | {amount_str:<12} | {desc}")

    print("=" * 80)


def calculate_totals(data):
    """
    Calculates total income and total expenses across all transactions.
    Returns a tuple: (total_income, total_expenses)
    """
    total_income = 0.0
    total_expenses = 0.0

    for item in data.get("transactions", []):
        amount = item.get("amount", 0.0)
        if item.get("type") == "income":
            total_income += amount
        elif item.get("type") == "expense":
            total_expenses += amount

    return round(total_income, 2), round(total_expenses, 2)


def calculate_balance(data):
    """
    Calculates available balance: Total Income - Total Expenses.
    """
    income, expenses = calculate_totals(data)
    return round(income - expenses, 2)


def display_financial_summary(data):
    """
    Displays the current totals and available balance to the user.
    """
    income, expenses = calculate_totals(data)
    balance = calculate_balance(data)

    print("\n" + "=" * 45)
    print("           FINANCIAL SUMMARY")
    print("=" * 45)
    print(f" Total Income:       ${income:>14,.2f}")
    print(f" Total Expenses:     ${expenses:>14,.2f}")
    print("-" * 45)
    status_label = "Surplus" if balance >= 0 else "DEFICIT"
    print(f" Available Balance:  ${balance:>14,.2f} ({status_label})")
    print("=" * 45)


# ==========================================
# STAGE 4: BUDGET MANAGEMENT & WARNING SYSTEM
# ==========================================

def get_monthly_expense_total(data, month):
    """
    Calculates total expenses for a given month (YYYY-MM).
    """
    month_expenses = 0.0
    for item in data.get("transactions", []):
        if item.get("type") == "expense" and item.get("date", "").startswith(month):
            month_expenses += item.get("amount", 0.0)
    return round(month_expenses, 2)


def set_monthly_budget(data, file_path=DATA_FILE):
    """
    Allows user to set or update a monthly spending budget limit.
    """
    print("\n--- [Set Monthly Spending Budget] ---")
    month = get_valid_month("Enter month to set budget for (YYYY-MM)")
    current_budget = data.get("monthly_budgets", {}).get(month)
    if current_budget is not None:
        print(f"Current budget for {month} is: ${current_budget:,.2f}")

    budget_amount = get_valid_amount(f"Enter budget limit for {month} ($): ")
    if "monthly_budgets" not in data:
        data["monthly_budgets"] = {}

    data["monthly_budgets"][month] = budget_amount
    if save_data(data, file_path):
        print(f"\n✓ Monthly budget for {month} successfully set to ${budget_amount:,.2f}.")

    # Evaluate against existing expenses
    check_budget_warning(data, month)


def check_budget_warning(data, month):
    """
    Checks if expenses for the given month exceed or approach the set budget.
    Prints appropriate warning messages.
    """
    budget = data.get("monthly_budgets", {}).get(month)
    if budget is None:
        return  # No budget set for this month

    spent = get_monthly_expense_total(data, month)

    if spent > budget:
        overage = spent - budget
        print("\n" + "!" * 60)
        print(f" [ALERT] BUDGET EXCEEDED FOR {month}!")
        print(f" Budget Limit:  ${budget:,.2f}")
        print(f" Total Spent:   ${spent:,.2f}")
        print(f" Over Budget:   ${overage:,.2f} ({((spent / budget) * 100):.1f}% spent)")
        print("!" * 60)
    elif spent >= (budget * 0.9):
        remaining = budget - spent
        print("\n" + "*" * 60)
        print(f" [WARNING] You have reached {((spent / budget) * 100):.1f}% of your budget for {month}!")
        print(f" Budget Limit:  ${budget:,.2f}")
        print(f" Total Spent:   ${spent:,.2f}")
        print(f" Remaining:     ${remaining:,.2f}")
        print("*" * 60)


# ==========================================
# STAGE 5: MONTHLY FINANCIAL REPORT
# ==========================================

def generate_monthly_report(data):
    """
    Generates a detailed monthly financial report including:
    - Monthly income, expenses, and net savings
    - Spending breakdown by category with percentages
    - Budget performance and remaining allowance
    """
    print("\n--- [Monthly Financial Report] ---")
    month = get_valid_month("Enter report month (YYYY-MM)")

    # Filter transactions for selected month
    month_transactions = [
        t for t in data.get("transactions", [])
        if t.get("date", "").startswith(month)
    ]

    if not month_transactions:
        print(f"\nNo transactions found for {month}.")
        return

    # Calculate month income and expenses
    month_income = sum(t["amount"] for t in month_transactions if t.get("type") == "income")
    month_expenses = sum(t["amount"] for t in month_transactions if t.get("type") == "expense")
    net_savings = month_income - month_expenses

    # Group expenses by category
    category_totals = {}
    for t in month_transactions:
        if t.get("type") == "expense":
            cat = t.get("category", "Uncategorized")
            category_totals[cat] = category_totals.get(cat, 0.0) + t.get("amount", 0.0)

    # Budget details
    budget = data.get("monthly_budgets", {}).get(month)

    print("\n" + "=" * 55)
    print(f"          FINANCIAL REPORT FOR {month}")
    print("=" * 55)
    print(f" Total Income:         ${month_income:>14,.2f}")
    print(f" Total Expenses:       ${month_expenses:>14,.2f}")
    print("-" * 55)
    savings_status = "Positive" if net_savings >= 0 else "Negative"
    print(f" Net Savings:          ${net_savings:>14,.2f} ({savings_status})")
    print("=" * 55)

    # Category Breakdown
    print("\n--- Expense Breakdown by Category ---")
    if category_totals:
        print(f"{'Category':<22} | {'Amount ($)':<12} | {'% of Expenses'}")
        print("-" * 55)
        for cat, amt in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            pct = (amt / month_expenses * 100) if month_expenses > 0 else 0.0
            print(f"{cat:<22} | ${amt:>10,.2f}  | {pct:>6.1f}%")
    else:
        print("No expenses recorded for this month.")

    # Budget Analysis
    print("\n--- Budget Status ---")
    if budget is not None:
        utilization = (month_expenses / budget * 100) if budget > 0 else 0.0
        remaining = budget - month_expenses
        print(f" Monthly Budget:       ${budget:>14,.2f}")
        print(f" Actual Spent:         ${month_expenses:>14,.2f}")
        print(f" Budget Used:           {utilization:>13.1f}%")
        if remaining >= 0:
            print(f" Remaining Allowance:  ${remaining:>14,.2f}")
        else:
            print(f" Over Budget By:       ${abs(remaining):>14,.2f} [EXCEEDED]")
    else:
        print(" No budget limit set for this month.")
        print(" (Use option 'Set Monthly Spending Budget' to configure a target)")

    print("=" * 55)
