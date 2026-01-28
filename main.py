expenses = []

# Load existing expenses from file
try:
    with open("expenses.txt", "r") as file:
        for line in file:
            parts=line.strip().split(",")
    
            if len(parts) !=2:
                continue

            amount,category= parts
            
            expenses.append({
                "amount": float(amount), 
                "category": category
            })
    
except FileNotFoundError:
    pass


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
            print("❌ Please enter a valid number for the amount.")
            continue
        category = input("Enter the expense category: ")

        expense = {
            "amount": amount,
            "category": category
        }

        expenses.append(expense)

        # Save to file
        with open("expenses.txt", "a") as file:
            file.write(f"{amount},{category}\n")

        print("✅ Expense saved!")

    elif choice == "2":
        print("\n📋 Your Expenses:")
        if not expenses:
            print("No expenses recorded yet.")
        else:
            total=0
            for e in expenses:
                print(f"- ${e['amount']:.2f} | {e['category']}")
                total += float(e["amount"])
            print(f"\n💰 Total spent: ${total:.2f}")

    elif choice == "3":
        print("Goodbye! 👋")
        break

    else:
        print("Invalid choice. Please try again.")



