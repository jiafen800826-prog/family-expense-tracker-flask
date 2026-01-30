from flask import Flask, render_template, request, redirect
import os
from collections import defaultdict
import json

app = Flask(__name__)
EXPENSE_FILE = "expenses.txt"

# Load expenses from file
def load_expenses():
    expenses = []
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) != 2:
                    continue
                amount, category = parts
                try:
                    amount = float(amount)
                except ValueError:
                    continue
                expenses.append({"amount": amount, "category": category})
    return expenses

# Save a new expense
def save_expense(amount, category):
    with open(EXPENSE_FILE, "a") as file:
        file.write(f"{amount},{category}\n")

# Delete an expense by index
def delete_expense(index):
    expenses = load_expenses()
    if 0 <= index < len(expenses):
        expenses.pop(index)
    with open(EXPENSE_FILE, "w") as file:
        for e in expenses:
            file.write(f"{e['amount']},{e['category']}\n")

# Main route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "delete" in request.form:
            index_to_delete = int(request.form["delete"])
            delete_expense(index_to_delete)
        else:
            amount = request.form["amount"]
            category = request.form["category"]
            try:
                amount = float(amount)
            except ValueError:
                return redirect("/")
            save_expense(amount, category)
        return redirect("/")

    expenses = load_expenses()
    total = sum(e["amount"] for e in expenses)

    # Calculate totals by category for chart
    category_totals = defaultdict(float)
    for e in expenses:
        category_totals[e["category"]] += e["amount"]

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        category_totals=json.dumps(category_totals)
    )

if __name__ == "__main__":
    app.run(debug=True)
