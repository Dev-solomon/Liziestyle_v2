import requests
import logging 
from flask import current_app as app, request, jsonify

app.logger.setLevel(logging.DEBUG)
# This is the single function implementing the required logic
# It accepts the web request object to correctly determine the client's IP.
def get_currency_symbol():
    """
    Determines the currency symbol ($ or €) based on the user's geographic location
    by resolving the client IP from the incoming request headers.
    """
    # 1. Get the Client IP address, prioritizing headers used by cloud proxies (e.g., Render)
    # X-Forwarded-For holds the client's original IP before it hits the proxy/load balancer.
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    # Fallback/default for non-US locations, as per the request
    currency_symbol = '€' 
    country_code = 'N/A'
    
    # 2. Use a Geolocation API (ip-api.com) to find the country
    try:
        geo_api_url = f"http://ip-api.com/json/{client_ip}"
        response = requests.get(geo_api_url, timeout=3)
        response.raise_for_status()
        geo_data = response.json()

        if geo_data.get('status') == 'success':
            country_code = geo_data.get('countryCode', 'N/A')
            app.logger.info(colored(f"SITE ACCESSED FROM: {country_code}", "cyan"))
            
            # 3. Determine the currency symbol
            if country_code == 'US':
                currency_symbol = '$'
            # else, it remains the default '€'

    except requests.RequestException:
        # If API fails or times out, we use the default (€)
        pass 

    return currency_symbol
