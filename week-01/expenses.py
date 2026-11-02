import json

EXPENSES_FILE = "week-01/expenses.json"
SUMMARY_FILE = "week-01/summary.json"
APPROVAL_LIMIT = 25000

# Loads JSON data from file
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

#  Dynamically groups and sums expenses by category
def calculate_category_totals(expenses):
    totals = {}
    for entry in expenses:
        category = entry["category"]
        amount = entry["amount"]
        totals[category] = totals.get(category, 0) + amount
    return totals

# Finds the single expense with the highest amount
def find_largest_expense(expenses):
    if not expenses:
        return None
    largest = expenses[0]
    for entry in expenses[1:]:
        if entry["amount"] > largest["amount"]:
            largest = entry
    return largest

#  Returns all expenses exceeding the approval limit
def filter_high_expenses(expenses, limit):
    return [entry for entry in expenses if entry["amount"] > limit]

# Formats an integer amount into comma-separated currency string
def format_rupees(amount):
    return f"Rs {amount:,}"

# Saves expense summary dictionary into a JSON file for the accountant
def save_summary(path, count, total, by_category):
    summary_data = {
        "expense_count": count,
        "total": total,
        "by_category": by_category,
    }
    with open(path, "w") as file:
        json.dump(summary_data, file, indent=2)

# Calculates summary values and prints the required formatted output
def print_report(expenses):
    total_spent = sum(entry["amount"] for entry in expenses)
    expense_count = len(expenses)
    categories = calculate_category_totals(expenses)
    largest = find_largest_expense(expenses)
    high_expenses = filter_high_expenses(expenses, APPROVAL_LIMIT)

    print("Cafe expense report")
    print(f"Expenses recorded: {expense_count}")
    print(f"Total spent: {format_rupees(total_spent)}")
    print()
    print("By category:")
    for cat, total in categories.items():
        print(f"  {cat:<10} Rs {total:>7,}")

    print()
    if largest:
        print(
            f"Largest expense: {largest['item']} ({format_rupees(largest['amount'])})"
        )

    print()
    print(f"Needs approval (over {format_rupees(APPROVAL_LIMIT)}): {len(high_expenses)}")
    for entry in high_expenses:
        print(f"  - {entry['item']}: {format_rupees(entry['amount'])}")

    save_summary(SUMMARY_FILE, expense_count, total_spent, categories)


def main():
    expenses = load_expenses(EXPENSES_FILE)
    if expenses is not None:
        print_report(expenses)


if __name__ == "__main__":
    main()