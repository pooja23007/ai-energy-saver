# ⚡ AI Energy Saver for Smart Homes

## Problem
Households waste electricity because appliances are used inefficiently. Examples are the AC left on when nobody is home, or heavy appliances run at peak hours.

## Solution
A web dashboard that analyses smart-plug readings, forecasts tomorrow's electricity use and recommends actions with estimated ₹ savings.

## AI Technologies Used
- **IoT analytics:** reads appliance-level readings and finds power used while nobody is home.
- **ML forecasting:** a Random Forest model forecasts the next 24 hours from past usage, temperature and occupancy.
- **AI recommendations:** combines the waste found and the forecast to suggest actions and savings.

## Features
- Tomorrow's forecast (kWh and ₹)
- Estimated monthly bill and possible saving
- Appliance-wise usage chart
- Waste-while-away chart
- Ranked recommendations
- Model accuracy (MAE) shown on the dashboard

## Tech Stack
Python, Flask, Pandas, scikit-learn, Chart.js, HTML/CSS/JavaScript

## Project Structure
- `generate_data.py`: simulates smart-plug data
- `analytics.py`: IoT analytics and waste detection
- `model.py`: ML forecasting model
- `recommendations.py`: recommendation engine
- `app.py`: Flask backend
- `templates/index.html`: dashboard

## How to Run
1. `pip install -r requirements.txt`
2. `python generate_data.py`
3. `python app.py`
4. Open http://127.0.0.1:5000

## Note
This is a software-only prototype. Smart-plug readings are simulated, and recommendation savings are estimates. With real IoT devices, only the data source would change.

## Live Demo
(Add your Render link here after deployment)
