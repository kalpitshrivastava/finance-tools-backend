from flask import Blueprint, request, jsonify

fd_bp = Blueprint("fd", __name__)

@fd_bp.route("/calculate", methods=["POST"])
def calculate_fd():
    data = request.get_json()
    try:
        P = float(data.get("principal", 0))
        R = float(data.get("annualInterestRate", 0)) / 100
        T = float(data.get("years", 0))
        n = 4  # quarterly compounding

        # Compound Interest formula
        A = P * (1 + R/n)**(n*T)

        return jsonify({
            "maturityAmount": round(A, 2),
            "totalInterest": round(A - P, 2),
            "principal": round(P, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)})
