from flask import Blueprint, request, jsonify
from math import pow

emi_bp = Blueprint("emi", __name__)

# Helper: Indian number formatting
def format_indian(amount):
    if amount >= 10000000:
        return f"{amount/10000000:.2f} Cr"
    elif amount >= 100000:
        return f"{amount/100000:.2f} L"
    else:
        return f"{amount:,.0f}"

@emi_bp.route("/calculate", methods=["POST"])
def calculate_emi():
    data = request.get_json()
    try:
        P = float(data.get("loanAmount", 0))
        R = float(data.get("interestRate", 0))
        N = int(data.get("tenureMonths", 0))
        loan_type = data.get("loanType", "reducing")  # "reducing" or "flat"
        prepayment = data.get("prepayment")  # dict: {"month": int, "amount": float}

        # Input validation
        if P <= 0 or R <= 0 or N <= 0:
            return jsonify({"error": "Invalid input values"}), 400
        if P > 100_000_000:
            return jsonify({"error": "Loan amount too high. Max 10 Cr."}), 400
        if N > 360:
            return jsonify({"error": "Tenure too long. Max 30 years."}), 400

        r = R / (12 * 100)  # monthly interest rate

        # EMI Calculation
        if loan_type == "flat":
            total_interest = P * R * N / (12 * 100)
            total_amount = P + total_interest
            emi = total_amount / N
        else:  # reducing balance
            emi = P * r * pow(1 + r, N) / (pow(1 + r, N) - 1)
            total_amount = emi * N
            total_interest = total_amount - P

        # Amortization schedule
        schedule = []
        balance = P
        for month in range(1, N + 1):
            if loan_type == "flat":
                interest = P * r
                principal_paid = emi - interest
            else:
                interest = balance * r
                principal_paid = emi - interest

            # Apply prepayment if exists
            if prepayment and month == prepayment.get("month"):
                extra = float(prepayment.get("amount", 0))
                principal_paid += extra
                balance -= extra

            balance -= principal_paid
            balance = max(balance, 0)  # avoid negative

            schedule.append({
                "month": month,
                "principalPaid": round(principal_paid, 2),
                "interestPaid": round(interest, 2),
                "remainingBalance": round(balance, 2),
                "principalPaidFormatted": format_indian(principal_paid),
                "interestPaidFormatted": format_indian(interest),
                "remainingBalanceFormatted": format_indian(balance)
            })

        return jsonify({
            "emi": round(emi, 2),
            "emiFormatted": format_indian(emi),
            "principal": round(P, 2),
            "principalFormatted": format_indian(P),
            "totalInterest": round(total_interest, 2),
            "totalInterestFormatted": format_indian(total_interest),
            "totalAmount": round(total_amount, 2),
            "totalAmountFormatted": format_indian(total_amount),
            "schedule": schedule,
            "loanType": loan_type
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
