"""Beginner-friendly budget recommendation using Scikit-learn Linear Regression."""
import numpy as np
from sklearn.linear_model import LinearRegression

def recommend_budget(total, category_totals):
    """Return a recommended budget and simple spending tips."""
    if total <= 0:
        return {
            "budget": 10000,
            "message": "Add expenses to receive a recommendation based on your spending.",
            "tips": [
                "Record expenses regularly.",
                "Set a monthly spending limit.",
                "Review your spending at the end of each week."
            ]
        }

    # Small demonstration dataset. Replace with real, anonymized monthly data
    # if your academic guide requires training on a project dataset.
    past_spending = np.array([5000, 7000, 9000, 11000, 13000, 15000]).reshape(-1, 1)
    suggested_budgets = np.array([6000, 8000, 10000, 12000, 14000, 16000])

    model = LinearRegression()
    model.fit(past_spending, suggested_budgets)
    prediction = float(model.predict(np.array([[total]]))[0])

    # A practical buffer: at least 10% above current spending.
    recommended = max(prediction, total * 1.10)
    recommended = int(round(recommended / 500) * 500)

    tips = []
    if category_totals:
        highest = max(category_totals, key=category_totals.get)
        share = category_totals[highest] / total * 100
        if share >= 35:
            tips.append(f"{highest} is {share:.0f}% of your spending, so consider setting a limit for it.")
            tips.append(f"Try reducing {highest} spending by 10% next month.")
        else:
            tips.append("Your expenses are spread across categories; keep tracking them.")
    if total >= 15000:
        tips.append("Try setting a weekly spending limit to avoid overspending.")
    else:
        tips.append("Check your spending once a week and adjust your plan if needed.")
    tips.append("Keep some money aside for unexpected expenses.")

    return {
        "budget": recommended,
        "message": "This estimate uses a simple Linear Regression model and your current expense totals.",
        "tips": tips
    }
