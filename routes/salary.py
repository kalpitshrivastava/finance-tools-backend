from flask import Blueprint, request, jsonify

salary_bp = Blueprint("salary", __name__)

@salary_bp.route("/calculate", methods=["POST"])
def calculate_salary():
    data = request.get_json()
    try:
        ctc = float(data.get("ctc", 0))
        basic = float(data.get("basicSalary", 0)) or 0.4 * ctc
        hra = float(data.get("hra", 0)) or 0.4 * basic
        other_allowances = float(data.get("otherAllowances", 0)) or ctc - basic - hra

        # Deductions
        pf = 0.12 * basic
        professional_tax = 200  # fixed

        taxable_income = ctc - pf - hra
        tax = 0
        # Simple tax slabs
        if taxable_income <= 250000:
            tax = 0
        elif taxable_income <= 500000:
            tax = (taxable_income - 250000) * 0.05
        elif taxable_income <= 1000000:
            tax = 12500 + (taxable_income - 500000) * 0.2
        else:
            tax = 112500 + (taxable_income - 1000000) * 0.3

        net_salary = ctc - pf - professional_tax - tax
        deductions = pf + professional_tax + tax

        # Pie chart breakdown
        breakdown = [
            {"name": "Basic", "value": basic},
            {"name": "HRA", "value": hra},
            {"name": "Other Allowances", "value": other_allowances},
            {"name": "PF", "value": pf},
            {"name": "Professional Tax", "value": professional_tax},
            {"name": "Income Tax", "value": tax},
        ]

        # Monthly net salary growth (simplified equal monthly)
        monthly_net = net_salary / 12
        monthlySalary = [{"month": i+1, "netSalary": monthly_net} for i in range(12)]

        return jsonify({
            "netSalary": round(net_salary, 2),
            "deductions": round(deductions, 2),
            "ctc": round(ctc, 2),
            "basic": round(basic, 2),
            "hra": round(hra, 2),
            "otherAllowances": round(other_allowances, 2),
            "pf": round(pf, 2),
            "professionalTax": round(professional_tax, 2),
            "taxableIncome": round(taxable_income, 2),
            "tax": round(tax, 2),
            "breakdown": breakdown,
            "monthlySalary": monthlySalary
        })
    except Exception as e:
        return jsonify({"error": str(e)})
