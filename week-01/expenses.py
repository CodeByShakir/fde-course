import json

EXPENSES_FILE = "week-01/expenses.json"
SUMMARY_FILE = "week-01/summary.json"
APPROVAL_LIMIT = 25000


def load_expenses(path):
    try:
        with open(path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Could not read {path}: file not found")
        return None
    except json.JSONDecodeError:
        print(f"Could not read {path}: invalid JSON format")
        return None


def calculate_category_totals(expenses):
    totals = {}
    for entry in expenses:
        category = entry["category"]
        amount = entry["amount"]
        if category in totals:
            totals[category] = totals[category] + amount
        else:
            totals[category] = amount
    return totals


def find_largest_expense(expenses):
    if len(expenses) == 0:
        return None
    largest = expenses[0]
    for entry in expenses:
        if entry["amount"] > largest["amount"]:
            largest = entry
    return largest


def filter_high_expenses(expenses, limit):
    flagged = []
    for entry in expenses:
        if entry["amount"] > limit:
            flagged.append(entry)
    return flagged


def save_summary(path, count, total, by_category):
    summary_data = {
        "expense_count": count,
        "total": total,
        "by_category": by_category
    }
    with open(path, "w") as file:
        json.dump(summary_data, file, indent=2)


def print_report(expenses):
    # 1. Calculate the overall total
    total_spent = 0
    for entry in expenses:
        total_spent = total_spent + entry["amount"]

    expense_count = len(expenses)
    categories = calculate_category_totals(expenses)
    largest = find_largest_expense(expenses)
    high_expenses = filter_high_expenses(expenses, APPROVAL_LIMIT)

    # 2. Print Header
    print("Cafe expense report")
    print(f"Expenses recorded: {expense_count}")
    print(f"Total spent: Rs {total_spent:,}")
    print()

    # 3. Print Categories
    print("By category:")
    for cat in categories:
        cat_amount = categories[cat]
        print(f"  {cat:<10} Rs {cat_amount:>7,}")

    # 4. Print Largest
    print()
    if largest is not None:
        name = largest["item"]
        amt = largest["amount"]
        print(f"Largest expense: {name} (Rs {amt:,})")

    # 5. Print Approval List
    print()
    print(f"Needs approval (over Rs {APPROVAL_LIMIT:,}): {len(high_expenses)}")
    for entry in high_expenses:
        item_name = entry["item"]
        item_amt = entry["amount"]
        print(f"  - {item_name}: Rs {item_amt:,}")

    # 6. Save the machine-readable file
    save_summary(SUMMARY_FILE, expense_count, total_spent, categories)


def main():
    expenses = load_expenses(EXPENSES_FILE)
    
    # Only run the report if the file loaded successfully without errors
    if expenses is not None:
        print_report(expenses)


if __name__ == "__main__":
    main()