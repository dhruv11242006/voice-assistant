def is_weather_request(text):
    weather_words = [
        "weather", "temperature", "cold", "hot",
        "raining", "sunny", "forecast", "wetter",
        "warm", "chilly", "humid", "wind"
    ]
    return any(word in text.lower() for word in weather_words)

def is_search_request(text):
    search_words = [
        "who is", "what is", "what are", "when did",
        "news", "latest", "current", "today",
        "happened", "score", "match", "results",
        "tell me about", "search", "look up"
    ]
    return any(phrase in text.lower() for phrase in search_words)

def extract_city(text, default="Paderborn"):
    cities = [
        "Paderborn", "Berlin", "London",
        "Paris", "New York", "Munich", "Hamburg"
    ]
    for city in cities:
        if city.lower() in text.lower():
            return city
    return default

def route_tools(text, get_weather_fn, search_fn):
    if is_weather_request(text):
        city = extract_city(text)
        print(f"Routing to weather: {city}")
        return get_weather_fn(city)

    if is_search_request(text):
        print(f"Routing to search: {text}")
        return search_fn(text)

    return None