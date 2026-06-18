import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask , render_template , redirect , url_for, request
from db.schema import init_db
init_db()
from db.queries import get_expenses_by_date, get_daily_total, get_yesterday_leftover , add_expense
import config
from budget.engine import get_budget_state


app = Flask(__name__)

def get_current_date_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")

@app.route("/")
def dashboard():
    today_str = get_current_date_str()
    
    expenses = get_expenses_by_date(today_str)
    total_spent = get_daily_total(today_str)
    yesterday_leftover = get_yesterday_leftover(today_str)
    
    effective_budget, remaining = get_budget_state(
        today_date=today_str,
        daily_budget=config.DAILY_BUDGET,
        rollover_enabled=config.ROLLOVER_ENABLED,
        yesterday_leftover=yesterday_leftover,
        amount_spent_today=total_spent
    )
    
    return render_template(
        "dashboard.html",
        expenses=expenses,
        total_spent=total_spent,
        remaining=remaining,
        effective_budget=effective_budget,
        daily_budget=config.DAILY_BUDGET,
        today_date=today_str,
        valid_categories = config.VALID_CATEGORIES
    )

@app.route("/add-expense", methods = ["POST"])
def add_expense_route():
    amount = float(request.form.get("amount", 0.0))
    category = request.form.get("category")
    description = request.form.get("description", "").strip()
    today_str = get_current_date_str()

    add_expense(
        date = today_str,
        amount = amount,
        category = category,
        source = "manual",
        raw_text = description
    )
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)