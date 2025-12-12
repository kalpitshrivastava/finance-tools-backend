from flask import Flask, jsonify
from flask_cors import CORS
from routes.emi import emi_bp
from routes.sip import sip_bp
from routes.fd import fd_bp
from routes.tax import tax_bp
from routes.salary import salary_bp

app = Flask(__name__)

# Allow both local and production frontend origins
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "https://finance-tools-oz9k.onrender.com"]}})

# Register blueprints
app.register_blueprint(emi_bp, url_prefix="/api/emi")
app.register_blueprint(sip_bp, url_prefix="/api/sip")
app.register_blueprint(fd_bp, url_prefix="/api/fd")
app.register_blueprint(tax_bp, url_prefix="/api/tax")
app.register_blueprint(salary_bp, url_prefix="/api/salary")

@app.route("/")
def home():
    return jsonify({"message": "Finance Tools API is running!"})

if __name__ == "__main__":
    # allow connections from other devices if needed
    app.run(debug=True, host="0.0.0.0", port=5000)
