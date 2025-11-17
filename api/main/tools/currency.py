from geopy.geocoders import Nominatim
import requests
from flask import current_app as app   # works inside Flask context

def get_currency_symbol():
    try:
        # Get IP location from ipinfo
        app.logger.debug("Fetching visitor IP geolocation from ipinfo.io")
        ip_data = requests.get("https://ipinfo.io/json").json()
        app.logger.debug(f"IP Data received: {ip_data}")

        loc = ip_data.get("loc")  # e.g. "37.7749,-122.4194"
        if loc:
            lat, lon = loc.split(",")
            app.logger.debug(f"Extracted lat/lon: {lat}, {lon}")

            # Reverse geocode
            geo = Nominatim(user_agent="geoapi")
            app.logger.debug("Sending coordinates to geopy for reverse lookup")
            location = geo.reverse(f"{lat}, {lon}", language='en')
            app.logger.debug(f"Reverse lookup result: {location.raw}")

            # Extract country code
            country = location.raw.get("address", {}).get("country_code", "").upper()
            app.logger.debug(f"Detected country code: {country}")

            # Return symbol based on country
            symbol = "$" if country == "US" else "€"
            app.logger.debug(f"Returning currency symbol: {symbol}")
            return symbol

        app.logger.debug("No location available, defaulting to €")
        return "€"
    
    except Exception as e:
        app.logger.debug(f"Error in get_currency_symbol: {e}")
        return "€"
