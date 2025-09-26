from scrapers.carsdotcom_scraper import scrape_carsdotcom
from scrapers.cargurus_scraper import scrape_cargurus
from etl import insert_cars, load_all_cars
from db import init_db

def run_carsdotcom():
    url = (
        "https://www.cars.com/shopping/results/"
        "?list_price_max=&makes[]=honda&maximum_distance=50"
        "&models[]=honda-civic&stock_type=used&zip=01721"
    )
    print("🔎 Scraping Cars.com...")
    cars = scrape_carsdotcom(url, max_listings=10)
    print(f"✅ Scraped {len(cars)} cars from Cars.com\n")

    # Print scraped results to console
    for c in cars:
        print(c)

    # Insert into DB if we got results
    if cars:
        insert_cars(cars, source="cars.com")
        print("\n💾 Inserted into DB.")
    else:
        print("⚠️ No cars scraped, DB not updated.")

def run_cargurus():
    url = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=d586&zip=01721"
    print("🔎 Scraping CarGurus...")
    cars = scrape_cargurus(url, max_listings=10, headless=False)
    print(f"✅ Scraped {len(cars)} cars from CarGurus\n")

    for c in cars:
        print(c)

    if cars:
        insert_cars(cars, source="cargurus")
        print("\n💾 Inserted into DB.")
    else:
        print("⚠️ No cars scraped, DB not updated.")

if __name__ == "__main__":
    init_db()  # always ensure DB exists
    run_carsdotcom()   # <- swap to run_cargurus() if testing CarGurus

    print("\n📊 Checking DB contents...")
    df = load_all_cars()
    print(df.head())