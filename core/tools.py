from ddgs import DDGS
import requests

def search(query):
    print(f"Searching for: {query}")

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            return "No results found"

        summary = ""

        for r in results:
            summary += r['title'] + " — " + r['body'] + "\n"

        return summary

    except Exception as e:
        print(f"Search failed: {e}")
        return ""

def get_weather(city="Paderborn"):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"

        geo_response = requests.get(geo_url).json()

        lat = geo_response["results"][0]["latitude"]
        lon = geo_response["results"][0]["longitude"]

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,weathercode,windspeed_10m"
            f"&temperature_unit=celsius"
        )

        weather_response = requests.get(weather_url).json()

        current = weather_response["current"]

        temp = current["temperature_2m"]
        wind = current["windspeed_10m"]
        code = current["weathercode"]

        weather_codes = {
            0: "clear sky",
            1: "mainly clear",
            2: "partly cloudy",
            3: "overcast",
            45: "foggy",
            48: "foggy",
            51: "light drizzle",
            61: "light rain",
            63: "moderate rain",
            71: "light snow",
            73: "moderate snow",
            80: "rain showers",
            95: "thunderstorm"
        }

        condition = weather_codes.get(code, "unknown conditions")

        return (
            f"Temperature: {temp}°C, "
            f"Condition: {condition}, "
            f"Wind: {wind} km/h"
        )

    except Exception as e:
        print(f"Weather failed: {e}")
        return "Couldn't get weather data."