import logging
import requests
from termcolor import colored
from flask import current_app as app, request

app.logger.setLevel(logging.DEBUG)

def get_currency_symbol():
    """
    Determines the currency symbol ($ or €) based on the user's geographic
    location by detecting the client IP and calling the ip-api.com geolocation API.
    Everything is contained inside this single function.
    """

    # ============================================================
    # 1. Extract client IP from headers (with fallbacks)
    # ============================================================
    client_ip = None

    # Check proxy headers in realistic order
    proxy_headers = [
        "X-Forwarded-For",    # Most common
        "CF-Connecting-IP",   # Cloudflare
        "X-Real-IP"           # Nginx / proxies
    ]

    for header in proxy_headers:
        value = request.headers.get(header)
        if value:
            client_ip = value.split(",")[0].strip()
            break

    # Fallback to Flask remote_addr
    if not client_ip:
        client_ip = request.remote_addr or "0.0.0.0"

    app.logger.debug(colored(f"[GeoIP] Resolved client IP: {client_ip}", "cyan"))

    # ============================================================
    # 2. Default currency before lookup
    # ============================================================
    currency_symbol = "€"
    country_code = "N/A"

    # Skip geolocation for local/dev IPs
    if client_ip in ("127.0.0.1", "::1", "0.0.0.0"):
        app.logger.debug(
            colored("[GeoIP] Local/unknown IP detected; using default currency €", "yellow")
        )
        return currency_symbol

    # ============================================================
    # 3. Perform API request
    # ============================================================
    try:
        url = f"http://ip-api.com/json/{client_ip}"
        app.logger.debug(colored(f"[GeoIP] Requesting: {url}", "blue"))

        response = requests.get(url, timeout=3)
        response.raise_for_status()

        data = response.json()
        app.logger.debug(colored(f"[GeoIP] Response JSON: {data}", "magenta"))

        if data.get("status") == "success":
            country_code = data.get("countryCode", "N/A")
            app.logger.info(
                colored(f"[GeoIP] Site accessed from: {country_code}", "green")
            )

            # ====================================================
            # 4. Decide currency based on countryCode
            # ====================================================
            if country_code == "US":
                currency_symbol = "$"
        else:
            app.logger.warning(
                colored(
                    f"[GeoIP] Lookup failure: status={data.get('status')}, message={data.get('message')}",
                    "yellow"
                )
            )

    except requests.RequestException as e:
        app.logger.error(colored(f"[GeoIP] API request error: {e}", "red"))

    except ValueError as e:
        app.logger.error(colored(f"[GeoIP] JSON decode error: {e}", "red"))

    # ============================================================
    # 5. Final log summary
    # ============================================================
    app.logger.debug(
        colored(
            f"[GeoIP] Final result => IP: {client_ip}, Country: {country_code}, Currency: {currency_symbol}",
            "cyan"
        )
    )

    return currency_symbol
