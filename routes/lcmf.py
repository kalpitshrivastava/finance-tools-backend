# backend/lcmf.py
from flask import Blueprint, request, jsonify

lcmf_bp = Blueprint("lcmf", __name__)

@lcmf_bp.route("/calculate", methods=["POST"])
def calculate_lcmf():
    """
    Life Cycle Money Flow Calculator
    Input JSON:
    {
        "ageStart": int,
        "ageEnd": int,
        "annualIncome": list of numbers,
        "annualExpenses": list of numbers,
        "annualInvestmentReturn": float (%)
    }
    Output:
    {
        "yearlyNetCashflow": [...],
        "totalSavings": float
    }
    """
    data = request.get_json()
    try:
        age_start = int(data.get("ageStart", 25))
        age_end = int(data.get("ageEnd", 65))
        income = data.get("annualIncome", [])
        expenses = data.get("annualExpenses", [])
        investment_return = float(data.get("annualInvestmentReturn", 5)) / 100

        n_years = age_end - age_start + 1

        # Fill missing years with last value
        if len(income) < n_years:
            income += [income[-1] if income else 0] * (n_years - len(income))
        if len(expenses) < n_years:
            expenses += [expenses[-1] if expenses else 0] * (n_years - len(expenses))

        savings = 0
        yearly_flow = []

        for i in range(n_years):
            net_cashflow = income[i] - expenses[i]
            savings = (savings + net_cashflow) * (1 + investment_return)
            yearly_flow.append({
                "year": age_start + i,
                "income": income[i],
                "expenses": expenses[i],
                "netCashflow": net_cashflow,
                "savings": round(savings, 2)
            })

        return jsonify({
            "yearlyNetCashflow": yearly_flow,
            "totalSavings": round(savings, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)})
