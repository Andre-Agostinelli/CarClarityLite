import requests
from bs4 import BeautifulSoup

def scrape_single_car(url, debug=True):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    if debug:
        with open("last_single_car.html", "w", encoding="utf-8") as f:
            f.write(r.text)
        print("💾 Saved HTML snapshot: last_single_car.html")

    title = soup.select_one("h1.listing-title").get_text(strip=True) if soup.select_one("h1.listing-title") else None
    price = soup.select_one("span.primary-price").get_text(strip=True) if soup.select_one("span.primary-price") else None
    mileage = soup.select_one("div.mileage").get_text(strip=True) if soup.select_one("div.mileage") else None

    result = {
        "title": title,
        "price": price,
        "mileage": mileage,
    }

    return result

if __name__ == "__main__":
    test_url = "https://www.cars.com/vehicledetail/12dcc9b8-99ff-4867-b31b-5f92382864d1/" #PUT_A_REAL_CARS.COM_LISTING_URL_HERE

    car = scrape_single_car(test_url, debug=True)
    print(car)
