from flask import Blueprint, request, jsonify

fd_bp = Blueprint("fd", __name__)

@fd_bp.route("/calculate", methods=["POST"])
def calculate_fd():
    data = request.get_json()
    try:
        P = float(data.get("principal", 0))
        R = float(data.get("annualInterestRate", 0)) / 100
        T = float(data.get("years", 0))
        n = int(data.get("compoundingPerYear", 4))  # quarterly default
        total_months = int(T * 12)

        # Maturity
        A = P * (1 + R/n)**(n*T)
        totalInterest = A - P

        # Growth details per month
        growthDetails = []
        principalAccumulated = P
        for month in range(1, total_months + 1):
            # Interest for this month (approx monthly compounding)
            interest = principalAccumulated * (R/12)
            principalAccumulated += interest
            growthDetails.append({
                "month": month,
                "principalAccumulated": round(principalAccumulated, 2),
                "interestAccumulated": round(principalAccumulated - P, 2)
            })

        # Max interest in a month
        maxInterestPerPeriod = round(P * (R/12), 2)

        effectiveAnnualYield = round(((1 + R/n)**n - 1)*100, 2)

        return jsonify({
            "maturityAmount": round(A, 2),
            "totalInterest": round(totalInterest, 2),
            "maxInterestPerPeriod": maxInterestPerPeriod,
            "effectiveAnnualYield": effectiveAnnualYield,
            "growthDetails": growthDetails
        })
    except Exception as e:
        return jsonify({"error": str(e)})
