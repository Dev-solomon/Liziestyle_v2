import requests
from flask import request

def get_currency_symbol():
    """
    Reads the user's IP from proxy headers (Render),
    looks up the country, and returns '$' if US, else '€'.
    """
    try:
        # 1. Get IP from common proxy headers
        xff = request.headers.get("X-Forwarded-For", "")
        if xff:
            # 'X-Forwarded-For' may be a comma-separated list: client, proxy1, proxy2, ...
            ip = xff.split(",")[0].strip()
        else:
            # Other possible headers used by some proxies/CDNs
            ip = (
                request.headers.get("CF-Connecting-IP")  # Cloudflare
                or request.headers.get("X-Real-IP")      # Nginx / some proxies
                or request.remote_addr                   # last resort (often Render IP)
            )

        if not ip:
            return "€"

        # 2. Geo lookup using the *client* IP, not Render's
        resp = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3)
        data = resp.json()
        country = data.get("country")

        # 3. Map country to currency symbol
        return "$" if country == "US" else "€"
    except Exception:
        # On any failure, default to €
        return "€"
