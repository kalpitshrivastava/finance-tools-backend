from flask import Blueprint, request, jsonify

emi_bp = Blueprint("emi", __name__)

@emi_bp.route("/calculate", methods=["POST"])
def calculate_emi():
    data = request.get_json()
    try:
        P = float(data.get("loanAmount", 0))      # Principal
        R = float(data.get("interestRate", 0))    # Annual rate %
        N = int(data.get("tenureMonths", 0))      # Tenure in months

        # Convert annual rate to monthly
        r = R / (12 * 100)

        # EMI formula
        emi = P * r * (1 + r)**N / ((1 + r)**N - 1)
        total_amount = emi * N
        total_interest = total_amount - P

        return jsonify({
            "emi": round(emi, 2),
            "totalInterest": round(total_interest, 2),
            "totalAmount": round(total_amount, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)})
