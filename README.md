# Personal Expense and Budget Tracker

A robust, interactive command-line application built with Python to help individuals track their income, monitor daily expenses, manage monthly budgets, and gain clear visibility into their financial health.

---

## 📌 Problem the Project Solves

Many individuals struggle with financial discipline, frequently asking themselves *"Where did all my money go at the end of the month?"* Without a structured tracking system, people often:
- Lose track of small, recurring daily expenses.
- Lack visibility into their net cash flow and true available balance.
- Unknowingly exceed their monthly spending limits until funds run dry.
- Lack actionable category breakdowns to identify spending leaks.

The **Personal Expense and Budget Tracker** solves this by providing a lightweight, frictionless, and completely offline CLI tool that persists records in JSON and alerts users when spending limits are approached or breached.

---

## 🎯 Project Objectives

- **Financial Clarity**: Provide real-time calculation of total earnings, total expenditures, and current available balance.
- **Budgetary Control**: Enable users to set monthly spending ceilings and receive automatic threshold alerts (warnings at 90% and alerts upon exceeding 100%).
- **Data Persistence & Integrity**: Safely store transactions and budget settings in a structured JSON file with automated recovery from corrupted or missing files.
- **Defensive Engineering**: Strictly validate all user inputs (preventing negative values, non-numeric strings, and invalid date formats).
- **Insightful Analytics**: Generate comprehensive monthly financial reports featuring category-wise expenditure breakdowns and budget utilization metrics.

---

## ✨ Features

1. **Add Income**: Record earnings with amount, category (Salary, Freelance, Investment, etc.), date, and description.
2. **Record Expenses**: Log outgoing transactions with automated classification into expense categories.
3. **Categorize Transactions**: Choose from standardized presets or add custom categories on the fly.
4. **View Transaction History**: Tabular view of all historical transactions with formatted IDs, dates, categories, +/- amount indicators, and notes.
5. **Calculate Totals & Balance**: Instantly computes total income, total expenses, and net surplus/deficit.
6. **Set Monthly Spending Budget**: Establish spending limits per month (`YYYY-MM`).
7. **Exceed Budget Warnings**: Automated alerts trigger immediately whenever an added expense causes monthly spending to exceed or approach (>=90%) the monthly budget.
8. **Monthly Financial Report**: Generates high-level summaries, category-wise percentages, and budget utilization rates for any specified month.
9. **JSON Data Persistence**: Automatic reading and writing to `data.json` with fallback defaults.

---

## 🛠 Technologies Used

- **Language**: Python 3.12+ (Standard Library only — zero external pip dependencies)
  - `json`: Data serialization and storage persistence.
  - `datetime`: Date validation, parsing, and formatting (`YYYY-MM-DD` and `YYYY-MM`).
  - `os`: File existence checks and path management.
  - `unittest`: Automated test suite for calculations, persistence, and edge cases.
- **Version Control**: Git & GitHub

---

## 📂 Project Structure

```text
personal-expense-tracker/
├── expense_tracker.py    # Core business logic, validation, and storage functions
├── main.py               # Interactive CLI loop and user menu
├── test_tracker.py       # Automated unit test suite
├── data.json             # Local JSON database (auto-generated on first run)
├── .gitignore            # Git exclusion rules
└── README.md             # Project documentation and user guide
```

---

## 🚀 Installation Instructions

### Prerequisites
- Python 3.8 or higher installed on your system. Verify with:
  ```bash
  python3 --version
  ```

### Clone the Repository
```bash
git clone https://github.com/smilinqremedy/real-world.git
cd real-world
```

*(No third-party packages are required; the application runs out of the box using Python's standard library).*

---

## 💻 How to Run the Application

Launch the command-line interface:

```bash
python3 main.py
```

To run the automated unit tests:

```bash
python3 -m unittest test_tracker.py
```

---

## 📖 Example Usage

### 1. Main Navigation Menu
```text
================================================
   PERSONAL EXPENSE & BUDGET TRACKER (CLI)   
================================================
 1. Add Income
 2. Record Expense
 3. View Transaction History
 4. View Totals and Available Balance
 5. Set Monthly Spending Budget
 6. Generate Monthly Financial Report
 7. Exit Application
================================================
Enter your choice (1-7):
```

### 2. Recording Income & Expense
```text
--- [Add Income] ---
Enter income amount ($): 3500.00
Select a category:
  1. Salary
  2. Freelance
  3. Investments
  4. Gift
  5. Other
  6. [Custom Category]
Choose category (1-6): 1
Enter date (YYYY-MM-DD) (default: 2026-11-19): 
Enter description: Monthly engineering salary

✓ Successfully recorded income of $3,500.00 under 'Salary'. (ID: 1)
```

### 3. Budget Alert Trigger
When an expense exceeds your allocated monthly limit:
```text
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 [ALERT] BUDGET EXCEEDED FOR 2026-11!
 Budget Limit:  $1,000.00
 Total Spent:   $1,150.00
 Over Budget:   $150.00 (115.0% spent)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

### 4. Monthly Financial Report
```text
=======================================================
          FINANCIAL REPORT FOR 2026-11
=======================================================
 Total Income:                 $      3,500.00
 Total Expenses:               $      1,150.00
-------------------------------------------------------
 Net Savings:                  $      2,350.00 (Positive)
=======================================================

--- Expense Breakdown by Category ---
Category               | Amount ($)   | % of Expenses
-------------------------------------------------------
Groceries              | $    650.00  |   56.5%
Rent/Mortgage          | $    350.00  |   30.4%
Utilities              | $    150.00  |   13.0%

--- Budget Status ---
 Monthly Budget:       $      1,000.00
 Actual Spent:         $      1,150.00
 Budget Used:                  115.0%
 Over Budget By:       $        150.00 [EXCEEDED]
=======================================================
```

---

## 🧪 Testing

The project includes unit test coverage for data serialization, ID generation, totals, balance, and edge cases (such as missing or corrupted JSON files):

```bash
python3 -m unittest test_tracker.py
```

Expected output:
```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.005s

OK
```
