"""
Personal Expense and Budget Tracker - Main Entry Point
Command-line interface with interactive loop and user menu.
"""

import sys
from expense_tracker import (
    load_data,
    add_income,
    add_expense,
    view_transactions,
    display_financial_summary,
    set_monthly_budget,
    generate_monthly_report,
    DATA_FILE
)


def display_menu():
    """
    Prints the main interactive menu options.
    """
    print("\n" + "=" * 48)
    print("   PERSONAL EXPENSE & BUDGET TRACKER (CLI)   ")
    print("=" * 48)
    print(" 1. Add Income")
    print(" 2. Record Expense")
    print(" 3. View Transaction History")
    print(" 4. View Totals and Available Balance")
    print(" 5. Set Monthly Spending Budget")
    print(" 6. Generate Monthly Financial Report")
    print(" 7. Exit Application")
    print("=" * 48)


def main():
    """
    Main execution loop for the CLI application.
    """
    print("\nStarting Personal Expense and Budget Tracker...")
    data = load_data(DATA_FILE)

    while True:
        try:
            display_menu()
            choice = input("Enter your choice (1-7): ").strip()

            if choice == "1":
                add_income(data, DATA_FILE)
            elif choice == "2":
                add_expense(data, DATA_FILE)
            elif choice == "3":
                view_transactions(data)
            elif choice == "4":
                display_financial_summary(data)
            elif choice == "5":
                set_monthly_budget(data, DATA_FILE)
            elif choice == "6":
                generate_monthly_report(data)
            elif choice == "7":
                print("\nThank you for managing your finances responsibly! Goodbye.\n")
                sys.exit(0)
            else:
                print("\n[Error] Invalid choice. Please enter a number between 1 and 7.")

        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user. Returning to menu...")
        except EOFError:
            print("\nExiting application. Goodbye.")
            sys.exit(0)


if __name__ == "__main__":
    main()
