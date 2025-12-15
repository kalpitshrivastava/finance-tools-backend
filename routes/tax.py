from flask import Blueprint, request, jsonify

tax_bp = Blueprint("tax", __name__)

@tax_bp.route("/calculate", methods=["POST"])
def calculate_tax():
    data = request.get_json()
    try:
        annual_income = float(data.get("annualIncome", 0))
        regime = data.get("regime", "old")  # "old" or "new"

        slab_info = []

        if regime == "old":
            # Old Regime FY 2025-26 slabs
            slabs = [
                (0, 250000, 0),
                (250001, 500000, 0.05),
                (500001, 1000000, 0.2),
                (1000001, float("inf"), 0.3)
            ]
        else:
            # New Regime FY 2025-26 slabs
            slabs = [
                (0, 300000, 0),
                (300001, 600000, 0.05),
                (600001, 900000, 0.1),
                (900001, 1200000, 0.15),
                (1200001, 1500000, 0.2),
                (1500001, float("inf"), 0.3)
            ]

        total_tax = 0

        for lower, upper, rate in slabs:
            if annual_income > lower:
                taxable = min(annual_income - lower, upper - lower)
                slab_tax = round(taxable * rate, 2)
                slab_info.append({
                    "slab": f"₹{int(lower)+1} - ₹{'∞' if upper==float('inf') else int(upper)}",
                    "taxableIncome": round(taxable, 2),
                    "taxRate": rate,
                    "tax": slab_tax
                })
                total_tax += slab_tax

        net_income = annual_income - total_tax

        return jsonify({
            "tax": round(total_tax, 2),
            "netIncome": round(net_income, 2),
            "slabs": slab_info
        })

    except Exception as e:
        return jsonify({"error": str(e)})
