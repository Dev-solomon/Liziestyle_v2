import requests
from termcolor import colored
from flask import request, current_app as app

def get_currency_symbol():
    try:
        # 1. Get the client IP (handles proxies/load balancers)
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if client_ip and ',' in client_ip:
            # If multiple IPs, take the first one
            client_ip = client_ip.split(',')[0].strip()
        app.logger.info(colored(f"Detected Client IP Address: {client_ip}", "yellow"))

        # 2. Query IP geolocation for that specific IP
        url = f"https://ipinfo.io/{client_ip}/json"
        #app.logger.debug(f"Requesting IP info from: {url}")
        resp = requests.get(url, timeout=2)
        data = resp.json()
        #app.logger.debug(f"IP info response: {data}")

        # 3. Get country code and choose symbol
        country = data.get("country", "").upper()
        app.logger.info(colored(f"Detected Country Code: {country}", "cyan"))
        # "€" - euro symbol
        symbol = "$" if country == "US" else "$"
        app.logger.info(colored(f"Returning Currency Symbol:=> {symbol}","cyan"))
        return symbol

    except Exception as e:
        app.logger.info(f"Error in get_currency_symbol: {e}")
        # Safe default
        return "$"
        
