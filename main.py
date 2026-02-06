expenses = []

# Load existing expenses from file
try:
    with open("expenses.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")

            if len(parts) != 2:
                continue

            amount, category = parts
            expenses.append({
                "amount": float(amount),
                "category": category
            })
except FileNotFoundError:
    pass


def calculate_total(expenses):
    def calculate_category_totals(expenses):
    totals = {}

    for e in expenses:
        category = e["category"]
        amount = e["amount"]

        if category in totals:
            totals[category] += amount
        else:
            totals[category] = amount

    return totals


print("Welcome to the Family Expense Tracker!")

while True:
    print("\n1. Add an expense")
    print("2. View expenses")
    print("3. Exit")

    choice = input("Choose an option (1, 2, or 3): ")

    if choice == "1":
        amount_input = input("Enter the expense amount: ")

        try:
            amount = float(amount_input)
        except ValueError:
            print("❌ Please enter a valid number.")
            continue

        category = input("Enter the expense category: ")

        expense = {
            "amount": amount,
            "category": category
        }

        expenses.append(expense)

        with open("expenses.txt", "a") as file:
            file.write(f"{amount},{category}\n")

        print("✅ Expense saved!")

    elif choice == "2":
        if not expenses:
            print("No expenses yet.")
        else:
            print("\nExpenses:")
            for e in expenses:
                print(f"- ${e['amount']:.2f} | {e['category']}")

            total = calculate_total(expenses)
            print(f"\nTotal spent: ${total:.2f}")

            category_totals = calculate_category_totals(expenses)
            print("\nBy category:")
            for category, amount in category_totals.items():
                print(f"{category}: ${amount:.2f}")

    elif choice == "3":
        print("Goodbye! 👋")
        break

    else:
        print("Invalid choice. Please try again.")
