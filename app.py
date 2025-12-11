from flask import Flask, jsonify
from flask_cors import CORS
from routes.emi import emi_bp  # your blueprint
from routes.sip import sip_bp
from routes.fd import fd_bp
from routes.tax import tax_bp
from routes.salary import salary_bp

# 1️⃣ Create app first
app = Flask(__name__)
CORS(app)

# 2️⃣ Then register blueprints
app.register_blueprint(emi_bp, url_prefix="/api/emi")
app.register_blueprint(sip_bp, url_prefix="/api/sip")
app.register_blueprint(fd_bp, url_prefix="/api/fd")
app.register_blueprint(tax_bp, url_prefix="/api/tax")
app.register_blueprint(salary_bp, url_prefix="/api/salary")

# 3️⃣ Define routes
@app.route("/")
def home():
    return jsonify({"message": "Finance Tools API is running!"})

# 4️⃣ Run app
if __name__ == "__main__":
    app.run(debug=True)
