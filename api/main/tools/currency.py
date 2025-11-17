import requests
from termcolor import colored


# Try to get User's Location
def get_country_code_from_ip():
    # 1) Try ipapi.co
    try:
        r = requests.get("https://ipapi.co/json/", timeout=5)
        if r.status_code == 200:
            data = r.json()
            code = data.get("country")
            if code:
                return code
        # if 429 or other issue, fall through to next provider
    except Exception:
        pass

    # 2) Try ipinfo.io
    try:
        r = requests.get("https://ipinfo.io/json", timeout=5)
        if r.status_code == 200:
            data = r.json()
            code = data.get("country")
            if code:
                return code
    except Exception:
        pass

    # 3) Try ipwho.is
    try:
        r = requests.get("https://ipwho.is/", timeout=5)
        if r.status_code == 200:
            data = r.json()
            code = data.get("country_code")
            if code:
                return code
    except Exception:
        pass

    # If everything fails
    return None
	
# Get the Exact Location of the Client Shopping to detech which currency to show
def get_currency_symbol():
    """
    Extracts user IP from request headers and returns
    '$' if IP is from the US, otherwise '€'.
    """
    try:
        # Extract IP from headers (works on Render)
        xff = request.headers.get("X-Forwarded-For")
        if xff:
            ip = xff.split(",")[0].strip()
        else:
            ip = getattr(request, "remote_addr", None) or getattr(request.client, "host", None)

        # Geo lookup
        res = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3)
        country = res.json().get("country")

        return "$" if country == "US" else "€"
    except:
        return "€"
