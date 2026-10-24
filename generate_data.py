import numpy as np
import pandas as pd

np.random.seed(42)
rows = []

for date in pd.date_range("2026-08-01", periods=60):
    weekend = date.dayofweek >= 5
    base_temp = np.random.uniform(26, 36)

    for hour in range(24):
        temp = base_temp + 4 * np.sin((hour - 9) * np.pi / 12) + np.random.normal(0, 1)
        home = 1 if (hour < 8 or hour >= 17 or weekend) else 0

        # AC: runs when hot and someone is home, sometimes left on when away (waste)
        ac_left_on = (home == 0 and temp > 30 and np.random.rand() < 0.35)
        ac = 0.0
        if temp > 27 and (home or ac_left_on):
            ac = 1.2 + 0.1 * (temp - 27) + np.random.normal(0, 0.1)

        fridge = 0.12 + np.random.normal(0, 0.01)
        heater = 0.9 if hour in (6, 7) else 0.0
        if home == 0 and np.random.rand() < 0.05:
            heater = 0.5  # left on by mistake
        washer = 0.5 if ((weekend and hour in (10, 11)) or
                         (not weekend and hour == 19 and np.random.rand() < 0.3)) else 0.0
        if home and (hour >= 18 or hour < 6):
            light = 0.2
        elif home:
            light = 0.05
        else:
            light = 0.03
        tv = 0.15 if (home and hour >= 18) else 0.05

        total = ac + fridge + heater + washer + light + tv
        rows.append([date.date(), hour, date.dayofweek, round(temp, 1), home,
                     round(ac, 3), round(fridge, 3), round(heater, 3),
                     round(washer, 3), round(light, 3), round(tv, 3), round(total, 3)])

cols = ["date", "hour", "day_of_week", "temperature", "occupancy",
        "ac", "fridge", "water_heater", "washing_machine", "lighting", "tv_others", "total_kwh"]
pd.DataFrame(rows, columns=cols).to_csv("energy_data.csv", index=False)
print("Done! Rows created:", len(rows))