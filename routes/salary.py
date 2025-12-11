from flask import Blueprint, request, jsonify

salary_bp = Blueprint("salary", __name__)

@salary_bp.route("/calculate", methods=["POST"])
def calculate_salary():
    data = request.get_json()
    try:
        ctc = float(data.get("ctc", 0))
        
        # Simplified breakup
        basic = 0.4 * ctc
        hra = 0.4 * basic
        pf = 0.12 * basic
        professional_tax = 200  # fixed, state-wise

        # Tax deduction via Income Tax Calculator logic (simplified)
        taxable_income = ctc - pf - hra
        tax = 0
        # For simplicity, using old regime slab for demonstration
        if taxable_income <= 250000:
            tax = 0
        elif taxable_income <= 500000:
            tax = (taxable_income - 250000) * 0.05
        elif taxable_income <= 1000000:
            tax = 12500 + (taxable_income - 500000) * 0.2
        else:
            tax = 112500 + (taxable_income - 1000000) * 0.3

        in_hand = ctc - pf - professional_tax - tax

        return jsonify({
            "basic": round(basic, 2),
            "hra": round(hra, 2),
            "pf": round(pf, 2),
            "professionalTax": round(professional_tax, 2),
            "tax": round(tax, 2),
            "inHand": round(in_hand, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)})
