import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def scrape_carsdotcom(search_url, max_listings=10, debug=True, headless=False):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0 Safari/537.36"
    )

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    driver.get(search_url)
    time.sleep(5)  # wait for Cars.com listings to render

    cards = driver.find_elements(By.CSS_SELECTOR, "div.vehicle-card")
    results = []

    if debug:
        with open("last_carsdotcom.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"💾 Saved debug snapshot: last_carsdotcom.html ({len(cards)} cards found)")

    for card in cards[:max_listings]:
        try:
            title_elem = card.find_element(By.CSS_SELECTOR, "h2.title")
            price_elem = card.find_element(By.CSS_SELECTOR, ".primary-price")
            mileage_elem = card.find_element(By.CSS_SELECTOR, ".mileage")

            title = title_elem.text.strip() if title_elem else None
            price = price_elem.text.strip() if price_elem else None
            mileage = mileage_elem.text.strip() if mileage_elem else None

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

    driver.quit()
    return results

if __name__ == "__main__":
    url = (
        "https://www.cars.com/shopping/results/"
        "?list_price_max=&makes[]=honda&maximum_distance=50"
        "&models[]=honda-civic&stock_type=used&zip=01721"
    )
    cars = scrape_carsdotcom(url, max_listings=5, debug=True, headless=False)
    for c in cars:
        print(c)
