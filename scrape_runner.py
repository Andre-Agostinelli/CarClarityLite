from scrapers.carsdotcom_scraper import scrape_carsdotcom
from scrapers.cargurus_scraper import scrape_cargurus
from etl import insert_cars, load_all_cars
from db import init_db

DEBUG = True  # toggle logging snapshots on/off

def run_carsdotcom():
    url = (
        "https://www.cars.com/shopping/results/"
        "?list_price_max=&makes[]=honda&maximum_distance=50"
        "&models[]=honda-civic&stock_type=used&zip=01721"
    )
    print("🔎 Scraping Cars.com...")
    cars = scrape_carsdotcom(url, max_listings=10, debug=DEBUG)
    print(f"✅ Scraped {len(cars)} cars from Cars.com\n")

    # Print scraped results to console
    for idx, c in enumerate(cars, 1):
        print(f"{idx}. {c}")

    if cars:
        insert_cars(cars, source="cars.com")
        print("\n💾 Inserted into DB.")
    else:
        print("⚠️ No cars scraped, DB not updated.")

def run_cargurus():
    url = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=d586&zip=01721"
    print("🔎 Scraping CarGurus...")
    cars = scrape_cargurus(url, max_listings=10, headless=False, debug=DEBUG)
    print(f"✅ Scraped {len(cars)} cars from CarGurus\n")

    for idx, c in enumerate(cars, 1):
        print(f"{idx}. {c}")

    if cars:
        insert_cars(cars, source="cargurus")
        print("\n💾 Inserted into DB.")
    else:
        print("⚠️ No cars scraped, DB not updated.")

if __name__ == "__main__":
    init_db()  # always ensure DB exists
    run_carsdotcom()   # swap with run_cargurus() if testing CarGurus

    print("\n📊 Checking DB contents...")
    df = load_all_cars()
    print(df.head())
