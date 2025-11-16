import requests


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
    country_code = get_country_code_from_ip()

    if country_code == "US":
        print(colored(f"Country Detected:=> {country_code}", "cyan"))
        return "$"
    elif country_code is None:
        # total failure – choose a default for your store
        print(colored(f"Country Detected Is None", "cyan"))
        return "€"   # or "$" depending on your main market
    else:
        # For now: anything not US → euro
        print(colored(f"Country Detected:=> {country_code}", "cyan"))
        return "€"