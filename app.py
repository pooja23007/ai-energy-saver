from flask import Flask, render_template, request, jsonify
from analytics import load_data, appliance_breakdown, hourly_pattern
from recommendations import get_recommendations
from model import MAE, R2

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/dashboard")
def dashboard():
    try:
        rate = float(request.args.get("rate", 8))
    except ValueError:
        rate = 8.0
    if rate <= 0:
        rate = 8.0

    result = get_recommendations(rate)
    df = load_data()
    result["appliances"] = appliance_breakdown(df)
    result["hourly_pattern"] = hourly_pattern(df)
    result["mae"] = MAE
    result["r2"] = R2
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)