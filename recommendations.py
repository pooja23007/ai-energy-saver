from analytics import load_data, find_waste, appliance_breakdown
from model import forecast_next_day


def get_recommendations(rate=8.0):
    df = load_data()
    days = df["date"].nunique()
    forecast = forecast_next_day()          # ML forecasting
    waste = find_waste(df, rate)            # IoT analytics

    tomorrow_kwh = round(sum(f["usage"] for f in forecast), 2)
    monthly_kwh = round(df["total_kwh"].sum() / days * 30, 1)
    tips = []

    # 1. Waste found by IoT analytics (top 3 appliances)
    for w in waste[:3]:
        tips.append({
            "title": f"Switch off {w['appliance']} when nobody is home",
            "detail": f"It uses {w['kwh_per_day']} kWh/day while the house is empty. "
                      "Use a smart-plug timer or auto-off.",
            "saving": w["monthly_cost"],
        })

    # 2. AC temperature (only the AC energy used while people are home)
    ac_home = df[df["occupancy"] == 1]["ac"].sum() / days
    tips.append({
        "title": "Set the AC 1 degree higher",
        "detail": "Roughly 6% less AC energy per degree (a common estimate).",
        "saving": round(ac_home * 0.06 * 30 * rate, 2),
    })

    # 3. Peak hours from the ML forecast
    peak = sorted(forecast, key=lambda f: f["usage"], reverse=True)[:3]
    hours = ", ".join(f"{h}:00" for h in sorted(p["hour"] for p in peak))
    tips.append({
        "title": "Avoid heavy appliances at peak hours",
        "detail": f"Tomorrow's forecast peaks at {hours}. "
                  "Run the washing machine and iron at other times to reduce load.",
        "saving": 0,
    })

    tips.sort(key=lambda t: t["saving"], reverse=True)

    return {
        "forecast": forecast,
        "tomorrow_kwh": tomorrow_kwh,
        "tomorrow_cost": round(tomorrow_kwh * rate, 2),
        "monthly_kwh": monthly_kwh,
        "monthly_bill": round(monthly_kwh * rate, 2),
        "waste": waste,
        "tips": tips,
        "total_saving": round(sum(t["saving"] for t in tips), 2),
    }


if __name__ == "__main__":
    r = get_recommendations(8.0)
    print("Tomorrow:", r["tomorrow_kwh"], "kWh = Rs", r["tomorrow_cost"])
    print("Estimated monthly bill: Rs", r["monthly_bill"])
    for t in r["tips"]:
        print("-", t["title"], "| saves Rs", t["saving"], "/month")
    print("Total possible saving: Rs", r["total_saving"], "/month")