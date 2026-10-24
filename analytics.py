import pandas as pd

APPLIANCES = ["ac", "fridge", "water_heater", "washing_machine", "lighting", "tv_others"]
NAMES = {
    "ac": "Air Conditioner",
    "fridge": "Refrigerator",
    "water_heater": "Water Heater",
    "washing_machine": "Washing Machine",
    "lighting": "Lighting",
    "tv_others": "TV & Others",
}


def load_data():
    return pd.read_csv("energy_data.csv")


def appliance_breakdown(df):
    """Total energy used by each appliance (kWh per day, average)."""
    days = df["date"].nunique()
    return {NAMES[a]: round(df[a].sum() / days, 2) for a in APPLIANCES}


def hourly_pattern(df):
    """Average total usage for each hour of the day."""
    avg = df.groupby("hour")["total_kwh"].mean().round(2)
    return [float(avg[h]) for h in range(24)]


def find_waste(df, rate):
    """Energy used while nobody is home (fridge is excluded, it must run)."""
    days = df["date"].nunique()
    away = df[df["occupancy"] == 0]
    waste = []
    for a in APPLIANCES:
        if a == "fridge":
            continue
        kwh_per_day = away[a].sum() / days
        if kwh_per_day > 0.01:
            waste.append({
                "appliance": NAMES[a],
                "kwh_per_day": round(kwh_per_day, 2),
                "monthly_cost": round(kwh_per_day * 30 * rate, 2),
            })
    waste.sort(key=lambda w: w["monthly_cost"], reverse=True)
    return waste


if __name__ == "__main__":
    df = load_data()
    print("Per appliance (kWh/day):", appliance_breakdown(df))
    print("Wasted while away (rate Rs 8/unit):")
    for w in find_waste(df, 8):
        print(" ", w)