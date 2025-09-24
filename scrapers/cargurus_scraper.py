import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_cargurus(search_url, max_listings=20, debug=True, headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(search_url)

    # Wait politely for listings (up to 15s)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='tileLayout']"))
        )
    except:
        print("⚠️ No listings found after wait. Possible captcha or site change.")
        if debug:
            with open("last_scrape.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
        driver.quit()
        return []

    time.sleep(2)  # give React a bit more time

    cards = driver.find_elements(By.CSS_SELECTOR, "div[class*='tileLayout']")
    results = []

    if not cards and debug:
        # Save HTML for debugging
        with open("last_scrape.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("⚠️ No listings found. Page HTML dumped to last_scrape.html")
        driver.quit()
        return []

    for card in cards[:max_listings]:
        try:
            # Try structured title
            try:
                title = card.find_element(By.CSS_SELECTOR, "div[class^='tileBody']").text.strip()
            except:
                title = card.text.strip()

            # Try price
            try:
                price = card.find_element(By.XPATH, ".//span[contains(text(),'$')]").text.strip()
            except:
                match = re.search(r"\$\s?[\d,]+", card.text)
                price = match.group(0) if match else "N/A"

            # Try structured props
            details = {}
            try:
                props = card.find_elements(By.CSS_SELECTOR, "dl[class^='propertiesList'] dt, dl[class^='propertiesList'] dd")
                for i in range(0, len(props), 2):
                    key = props[i].text.strip().replace(":", "")
                    val = props[i+1].text.strip()
                    details[key] = val
            except:
                pass

            # Fallbacks
            year = details.get("Year")
            make = details.get("Make")
            model = details.get("Model")
            mileage = details.get("Mileage")

            if not year:
                match = re.search(r"\b(19|20)\d{2}\b", title)
                year = match.group(0) if match else None
            if not make and title:
                parts = title.split()
                if len(parts) > 1:
                    make = parts[1]
            if not model and title:
                parts = title.split()
                if len(parts) > 2:
                    model = " ".join(parts[2:4])  # crude fallback
            if not mileage:
                match = re.search(r"([\d,]+)\s+miles", card.text)
                mileage = match.group(1).replace(",", "") if match else None

            results.append({
                "title": title,
                "price": price,
                "year": year,
                "make": make,
                "model": model,
                "trim": details.get("Trim"),
                "mileage": mileage,
                "body": details.get("Body type"),
                "fuel": details.get("Fuel type"),
                "mpg": details.get("Combined gas mileage"),
                "color": details.get("Exterior color")
            })
        except Exception as e:
            print("Parse error:", e)

    driver.quit()
    return results

if __name__ == "__main__":
    url = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=d586&zip=01721"
    cars = scrape_cargurus(url, max_listings=5, headless=False)
    for c in cars:
        print(c)
