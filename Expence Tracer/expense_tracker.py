import argparse
import json
import os
from datetime import datetime

DATA_FILE = 'expenses.json'

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_expenses(expenses):
    with open(DATA_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)

def add_expense(description, amount, category):
    if amount <= 0:
        print("Error: Amount must be greater than zero.")
        return
    
    expenses = load_expenses()
    new_id = max([e['id'] for e in expenses], default=0) + 1
    
    new_expense = {
        "id": new_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": description,
        "amount": amount,
        "category": category
    }
    
    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {new_id})")

def list_expenses(category_filter=None):
    expenses = load_expenses()
    print(f"{'ID':<4} {'Date':<12} {'Description':<15} {'Amount':<10} {'Category':<10}")
    print("-" * 55)
    
    for e in expenses:
        if category_filter and e.get('category') != category_filter:
            continue
        print(f"{e['id']:<4} {e['date']:<12} {e['description']:<15} ${e['amount']:<9} {e.get('category', 'N/A'):<10}")

def delete_expense(expense_id):
    expenses = load_expenses()
    updated_expenses = [e for e in expenses if e['id'] != expense_id]
    
    if len(expenses) == len(updated_expenses):
        print(f"Error: Expense with ID {expense_id} not found.")
    else:
        save_expenses(updated_expenses)
        print("Expense deleted successfully")

def show_summary(month=None):
    expenses = load_expenses()
    current_year = datetime.now().year
    
    if month:
        if not (1 <= month <= 12):
            print("Error: Month must be between 1 and 12.")
            return
        filtered = [e for e in expenses if datetime.strptime(e['date'], "%Y-%m-%d").month == month 
                    and datetime.strptime(e['date'], "%Y-%m-%d").year == current_year]
        total = sum(e['amount'] for e in filtered)
        month_name = datetime(2000, month, 1).strftime('%B')
        print(f"Total expenses for {month_name}: ${total}")
    else:
        total = sum(e['amount'] for e in expenses)
        print(f"Total expenses: ${total}")

def export_to_csv():
    expenses = load_expenses()
    import csv
    with open('expenses_export.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "date", "description", "amount", "category"])
        writer.writeheader()
        writer.writerows(expenses)
    print("Expenses exported to expenses_export.csv")

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('--description', required=True)
    add_parser.add_argument('--amount', type=float, required=True)
    add_parser.add_argument('--category', default="General")

    # List command
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('--category', help="Filter by category")

    # Delete command
    del_parser = subparsers.add_parser('delete')
    del_parser.add_argument('--id', type=int, required=True)

    # Summary command
    sum_parser = subparsers.add_parser('summary')
    sum_parser.add_argument('--month', type=int, help="Month number (1-12)")

    # Export command
    subparsers.add_parser('export')

    args = parser.parse_args()

    if args.command == 'add':
        add_expense(args.description, args.amount, args.category)
    elif args.command == 'list':
        list_expenses(args.category)
    elif args.command == 'delete':
        delete_expense(args.id)
    elif args.command == 'summary':
        show_summary(args.month)
    elif args.command == 'export':
        export_to_csv()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()