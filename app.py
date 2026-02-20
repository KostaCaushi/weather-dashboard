from flask import Flask, render_template, request
from dotenv import load_dotenv
from weather import get_current_weather, get_forecast

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    city = ""
    error = ""
    current = None
    forecast = []

    if request.method == "POST":
        city = (request.form.get("city") or "").strip()

        if not city:
            error = "Please enter a city."
            return render_template("index.html", city=city, error=error, current=current, forecast=forecast)

        current_data = get_current_weather(city)

        if not current_data["ok"]:
            error = current_data.get("error", "Could not fetch weather data.")
        else:
            data = current_data["data"]
            current = {
                "name": data.get("name", city),
                "country": data.get("sys", {}).get("country", ""),
                "temp": round(data["main"]["temp"], 1),
                "feels_like": round(data["main"]["feels_like"], 1),
                "humidity": data["main"]["humidity"],
                "desc": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["icon"],
                "wind": round(data.get("wind", {}).get("speed", 0), 1)
            }

            forecast_data = get_forecast(city)
            if forecast_data["ok"]:
                forecast = forecast_data["data"]
            else:
                forecast = []

    return render_template("index.html", city=city, error=error, current=current, forecast=forecast)

if __name__ == "__main__":
    app.run(debug=True)