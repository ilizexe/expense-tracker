from flask import Flask, render_template, request, redirect
from datetime import date

app = Flask(__name__)

expenses = []
CATEGORIES = ["Salary", "Investment", "Food", "Transport", "Housing", "Entertainment", "Utilities", "Other"]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "Cash", "Bank Transfer", "UPI"]

def calculate_metrics():
    total_income = sum(item["amount"] for item in expenses if item["type"] == "income")
    total_expense = sum(item["amount"] for item in expenses if item["type"] == "expense")
    net_cash_flow = total_income - total_expense
    savings_rate = (net_cash_flow / total_income * 100) if total_income > 0 else 0.0
    return total_income, total_expense, net_cash_flow, savings_rate

@app.route("/")
def home():
    return render_dashboard()

@app.route("/edit/<int:index>")
def edit_expense(index):
    if 0 <= index < len(expenses):
        return render_dashboard(edit_index=index)
    return redirect("/")

def render_dashboard(edit_index=None):
    total_income, total_expense, net_cash_flow, savings_rate = calculate_metrics()

    category_totals = {cat: 0.0 for cat in CATEGORIES}
    for item in expenses:
        if item["type"] == "expense":
            cat = item.get("category", "Other")
            category_totals[cat] += item["amount"]

    edit_item = expenses[edit_index] if edit_index is not None and 0 <= edit_index < len(expenses) else None

    return render_template(
        "index.html",
        expenses=expenses,
        total_income=total_income,
        total_expense=total_expense,
        net_cash_flow=net_cash_flow,
        savings_rate=savings_rate,
        categories=CATEGORIES,
        payment_methods=PAYMENT_METHODS,
        category_labels=list(category_totals.keys()),
        category_values=list(category_totals.values()),
        today_date=date.today().isoformat(),
        edit_index=edit_index,
        edit_item=edit_item
    )

@app.route("/add", methods=["POST"])
def add_expense():
    entry = {
        "title": request.form.get("title"),
        "amount": float(request.form.get("amount")),
        "type": request.form.get("type"),
        "category": request.form.get("category"),
        "payment_method": request.form.get("payment_method"),
        "date": request.form.get("date") or date.today().isoformat()
    }
    expenses.append(entry)
    return redirect("/")

@app.route("/update/<int:index>", methods=["POST"])
def update_expense(index):
    if 0 <= index < len(expenses):
        expenses[index] = {
            "title": request.form.get("title"),
            "amount": float(request.form.get("amount")),
            "type": request.form.get("type"),
            "category": request.form.get("category"),
            "payment_method": request.form.get("payment_method"),
            "date": request.form.get("date") or date.today().isoformat()
        }
    return redirect("/")

@app.route("/delete/<int:index>", methods=["POST"])
def delete_expense(index):
    if 0 <= index < len(expenses):
        expenses.pop(index)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)