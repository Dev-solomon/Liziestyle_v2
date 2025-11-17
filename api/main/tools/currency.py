import requests
import logging
from termcolor import colored
from flask import current_app as app, request

app.logger.setLevel(logging.DEBUG)

def get_currency_symbol():
    """
    Determines the currency symbol ($ or €) based on the user's geographic location
    by resolving the client IP from the incoming request headers.
    """

    # 1. Extract the client IP (X-Forwarded-For is used by reverse proxies like Render)
    client_ip_header = request.headers.get('X-Forwarded-For')
    if client_ip_header:
        client_ip = client_ip_header.split(',')[0].strip()
    else:
        client_ip = request.remote_addr or "0.0.0.0"

    app.logger.debug(f"Resolved client IP: {client_ip}")

    # Default currency
    currency_symbol = '€'
    country_code = 'N/A'

    # 2. Query the geolocation API
    try:
        geo_api_url = f"http://ip-api.com/json/{client_ip}"
        response = requests.get(geo_api_url, timeout=3)
        response.raise_for_status()

        geo_data = response.json()

        if geo_data.get('status') == 'success':
            country_code = geo_data.get('countryCode', 'N/A')
            app.logger.info(f"SITE ACCESSED FROM: {country_code}")

            # 3. Decide currency
            if country_code == 'US':
                currency_symbol = '$'

    except requests.RequestException as e:
        app.logger.error(f"Geo API request failed: {e}")

    return currency_symbol
