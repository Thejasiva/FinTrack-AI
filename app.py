from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import date
from collections import defaultdict
from ml_recommendation import recommend_budget

app = Flask(__name__)
app.secret_key = "fintrack-ai-local-demo-key"
DB_NAME = "finance.db"

CATEGORIES = [
    "Food", "Transport", "Shopping", "Bills",
    "Entertainment", "Healthcare", "Education", "Other"
]

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                expense_date TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                month TEXT PRIMARY KEY,
                amount REAL NOT NULL CHECK(amount >= 0)
            )
        """)

def get_month_expenses(month):
    with get_db() as conn:
        return conn.execute("""
            SELECT id, title, amount, category, expense_date
            FROM expenses
            WHERE substr(expense_date, 1, 7) = ?
            ORDER BY expense_date DESC, id DESC
        """, (month,)).fetchall()

@app.route("/")
def index():
    current_month = date.today().strftime("%Y-%m")
    expenses = get_month_expenses(current_month)
    category_totals = defaultdict(float)

    for expense in expenses:
        category_totals[expense["category"]] += expense["amount"]

    total = sum(category_totals.values())
    with get_db() as conn:
        row = conn.execute(
            "SELECT amount FROM budgets WHERE month = ?", (current_month,)
        ).fetchone()

    budget = row["amount"] if row else 0
    remaining = budget - total if row else 0
    recommendation = recommend_budget(total, dict(category_totals))

    return render_template(
        "index.html",
        expenses=expenses,
        categories=CATEGORIES,
        current_month=current_month,
        total=round(total, 2),
        budget=round(budget, 2),
        remaining=round(remaining, 2),
        recommendation=recommendation,
        chart_labels=list(category_totals.keys()),
        chart_values=[round(value, 2) for value in category_totals.values()]
    )

@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "")
    expense_date = request.form.get("expense_date", "")
    amount_text = request.form.get("amount", "").strip()

    try:
        amount = float(amount_text)
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        flash("Enter an amount greater than zero.", "error")
        return redirect(url_for("index"))

    try:
        date.fromisoformat(expense_date)
    except ValueError:
        flash("Choose a valid expense date.", "error")
        return redirect(url_for("index"))

    if not title or len(title) > 100 or category not in CATEGORIES:
        flash("Enter an expense name and choose a valid category.", "error")
        return redirect(url_for("index"))

    with get_db() as conn:
        conn.execute(
            "INSERT INTO expenses (title, amount, category, expense_date) VALUES (?, ?, ?, ?)",
            (title, amount, category, expense_date)
        )

    flash("Expense added successfully.", "success")
    return redirect(url_for("index"))

@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    with get_db() as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    flash("Expense deleted.", "success")
    return redirect(url_for("index"))

@app.route("/budget", methods=["POST"])
def save_budget():
    month = request.form.get("month", "")
    amount_text = request.form.get("budget", "").strip()

    try:
        date.fromisoformat(month + "-01")
        amount = float(amount_text)
        if amount < 0:
            raise ValueError
    except (ValueError, TypeError):
        flash("Enter a valid month and a budget of zero or more.", "error")
        return redirect(url_for("index"))

    with get_db() as conn:
        conn.execute("""
            INSERT INTO budgets (month, amount) VALUES (?, ?)
            ON CONFLICT(month) DO UPDATE SET amount = excluded.amount
        """, (month, amount))

    flash("Monthly budget saved.", "success")
    return redirect(url_for("index"))

@app.route("/report")
def report():
    current_month = date.today().strftime("%Y-%m")
    expenses = get_month_expenses(current_month)
    category_totals = defaultdict(float)

    for expense in expenses:
        category_totals[expense["category"]] += expense["amount"]

    total = sum(category_totals.values())
    highest_category = max(category_totals, key=category_totals.get) if category_totals else "None"
    recommendation = recommend_budget(total, dict(category_totals))

    return render_template(
        "report.html",
        current_month=current_month,
        category_totals=dict(category_totals),
        total=round(total, 2),
        highest_category=highest_category,
        recommendation=recommendation
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
