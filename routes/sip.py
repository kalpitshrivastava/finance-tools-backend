from flask import Blueprint, request, jsonify

sip_bp = Blueprint("sip", __name__)

@sip_bp.route("/calculate", methods=["POST"])
def calculate_sip():
    data = request.get_json()
    try:
        SIP = float(data.get("monthlyInvestment", 0))
        rate = float(data.get("annualInterestRate", 0)) / 100
        years = int(data.get("years", 0))

        n = 12  # monthly compounding
        months = years * 12
        r = rate / 12

        # Future Value of SIP
        fv = SIP * (((1 + r)**months - 1) / r) * (1 + r)

        return jsonify({
            "corpus": round(fv, 2),
            "investment": round(SIP * months, 2),
            "returns": round(fv - (SIP * months), 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)})
