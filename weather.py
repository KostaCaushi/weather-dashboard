from datetime import datetime
import os
import requests

BASE_URL = "https://api.openweathermap.org/data/2.5"


def get_current_weather(city: str) -> dict:
    api_key = os.getenv("OPENWEATHER_API_KEY")

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(f"{BASE_URL}/weather", params=params, timeout=10)

    if response.status_code != 200:
        return {
            "ok": False,
            "status": response.status_code,
            "error": response.json().get("message", "Error fetching weather"),
            "data": None
        }

    return {
        "ok": True,
        "status": 200,
        "data": response.json()
    }


def get_forecast(city: str) -> dict:
    api_key = os.getenv("OPENWEATHER_API_KEY")

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(f"{BASE_URL}/forecast", params=params, timeout=10)

    if response.status_code != 200:
        return {
            "ok": False,
            "status": response.status_code,
            "error": response.json().get("message", "Error fetching forecast"),
            "data": None
        }

    data = response.json()
    items = data.get("list", [])

    daily = {}

    for item in items:
        dt_txt = item.get("dt_txt", "")
        if not dt_txt:
            continue

        date = dt_txt.split(" ")[0]
        hour = dt_txt.split(" ")[1][:2]

        # Prefer 12:00 data points
        score = 2 if hour == "12" else 1

        entry = {
            "date": date,
            "date_label": datetime.strptime(date, "%Y-%m-%d").strftime("%a, %b %d"),
            "temp": round(item["main"]["temp"], 1),
            "humidity": item["main"]["humidity"],
            "desc": item["weather"][0]["description"].title(),
            "icon": item["weather"][0]["icon"],
            "_score": score
        }

        if date not in daily or entry["_score"] > daily[date]["_score"]:
            daily[date] = entry

    forecast_list = sorted(daily.values(), key=lambda x: x["date"])[:5]

    for d in forecast_list:
        d.pop("_score", None)

    return {
        "ok": True,
        "status": 200,
        "data": forecast_list
    }