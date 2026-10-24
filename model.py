import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

FEATURES = ["hour", "day_of_week", "temperature", "occupancy", "lag_24", "lag_168"]

raw = pd.read_csv("energy_data.csv")

# Past-consumption features: same hour yesterday and same hour last week
data = raw.copy()
data["lag_24"] = data["total_kwh"].shift(24)
data["lag_168"] = data["total_kwh"].shift(168)
data = data.dropna().reset_index(drop=True)

# Test on the last 7 days, which the model has never seen
train = data.iloc[:-168]
test = data.iloc[-168:]

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(train[FEATURES], train["total_kwh"])

pred = model.predict(test[FEATURES])
MAE = round(float(mean_absolute_error(test["total_kwh"], pred)), 3)
R2 = round(float(r2_score(test["total_kwh"], pred)), 3)

# After testing, retrain on all the data
model.fit(data[FEATURES], data["total_kwh"])


def forecast_next_day():
    """Forecast hourly usage (kWh) for the day after the last reading."""
    next_dow = (int(raw["day_of_week"].iloc[-1]) + 1) % 7
    last7 = raw.iloc[-168:]
    avg_temp = last7.groupby("hour")["temperature"].mean()
    occ = raw.groupby(["day_of_week", "hour"])["occupancy"].mean().round()

    result = []
    for h in range(24):
        row = pd.DataFrame([[
            h, next_dow, float(avg_temp[h]), float(occ[(next_dow, h)]),
            float(raw["total_kwh"].iloc[-24 + h]),
            float(raw["total_kwh"].iloc[-168 + h]),
        ]], columns=FEATURES)
        result.append({"hour": h, "usage": round(float(model.predict(row)[0]), 2)})
    return result


if __name__ == "__main__":
    print("Model accuracy on unseen 7 days:")
    print("  MAE (avg error):", MAE, "kWh per hour")
    print("  R2 score:", R2)
    f = forecast_next_day()
    print("Tomorrow's total forecast:", round(sum(x["usage"] for x in f), 2), "kWh")
    print(f)