from flask import Blueprint, request, jsonify

tax_bp = Blueprint("tax", __name__)

@tax_bp.route("/calculate", methods=["POST"])
def calculate_tax():
    data = request.get_json()
    try:
        annual_income = float(data.get("annualIncome", 0))
        regime = data.get("regime", "old")  # "old" or "new"
        tax = 0

        if regime == "old":
            # Old Regime FY 2025-26 slabs (example)
            if annual_income <= 250000:
                tax = 0
            elif annual_income <= 500000:
                tax = (annual_income - 250000) * 0.05
            elif annual_income <= 1000000:
                tax = 12500 + (annual_income - 500000) * 0.2
            else:
                tax = 112500 + (annual_income - 1000000) * 0.3
        else:
            # New Regime FY 2025-26 slabs (example)
            if annual_income <= 300000:
                tax = 0
            elif annual_income <= 600000:
                tax = (annual_income - 300000) * 0.05
            elif annual_income <= 900000:
                tax = 15000 + (annual_income - 600000) * 0.1
            elif annual_income <= 1200000:
                tax = 45000 + (annual_income - 900000) * 0.15
            elif annual_income <= 1500000:
                tax = 90000 + (annual_income - 1200000) * 0.2
            else:
                tax = 150000 + (annual_income - 1500000) * 0.3

        tax = round(tax, 2)
        net_income = annual_income - tax

        return jsonify({
            "tax": tax,
            "netIncome": net_income
        })

    except Exception as e:
        return jsonify({"error": str(e)})
