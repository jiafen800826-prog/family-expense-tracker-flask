from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict

app = Flask(__name__)

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

# Home page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        new_expense = Expense(
            amount=float(request.form["amount"]),
            category=request.form["category"]
        )
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for("index"))

    expenses = Expense.query.all()
    total = sum(e.amount for e in expenses)

    category_totals = defaultdict(float)
    for e in expenses:
        category_totals[e.category] += e.amount

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        category_totals=dict(category_totals)
    )

# Update expense (AJAX)
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    expense = Expense.query.get_or_404(id)
    data = request.get_json()
    expense.amount = float(data["amount"])
    expense.category = data["category"]
    db.session.commit()
    return jsonify(success=True)

# Delete one
@app.route("/delete/<int:id>")
def delete(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify(success=True)

# Delete all
@app.route("/delete_all")
def delete_all():
    Expense.query.delete()
    db.session.commit()
    return jsonify(success=True)

# Chart data
@app.route("/data")
def data():
    expenses = Expense.query.all()
    total = sum(e.amount for e in expenses)

    category_totals = defaultdict(float)
    for e in expenses:
        category_totals[e.category] += e.amount

    return jsonify(
        total=total,
        category_totals=category_totals
    )


if __name__ == "__main__":
    app.run(debug=True)

