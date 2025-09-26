import requests
from bs4 import BeautifulSoup

def scrape_carsdotcom(search_url, max_listings=20, debug=True):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        r = requests.get(search_url, headers=headers, timeout=15)  # timeout added
        r.raise_for_status()
    except Exception as e:
        print("⚠️ Request failed:", e)
        return []

    soup = BeautifulSoup(r.text, "html.parser")

    cards = soup.select("div.vehicle-card")
    results = []

    if not cards and debug:
        with open("last_carsdotcom.html", "w", encoding="utf-8") as f:
            f.write(r.text)
        print("⚠️ No listings found. Saved HTML for debugging.")
        return []

    for card in cards[:max_listings]:
        try:
            title = card.select_one("h2.title").get_text(strip=True) if card.select_one("h2.title") else None
            price = card.select_one(".primary-price").get_text(strip=True) if card.select_one(".primary-price") else None
            mileage = card.select_one(".mileage").get_text(strip=True) if card.select_one(".mileage") else None

            # crude parse from title
            year, make, model = None, None, None
            if title:
                parts = title.split()
                if parts and parts[0].isdigit():
                    year = parts[0]
                    if len(parts) > 1:
                        make = parts[1]
                    if len(parts) > 2:
                        model = " ".join(parts[2:])

            results.append({
                "title": title,
                "price": price,
                "year": year,
                "make": make,
                "model": model,
                "trim": None,
                "mileage": mileage,
                "body": None,
                "fuel": None,
                "mpg": None,
                "color": None
            })
        except Exception as e:
            print("Parse error:", e)

    return results
