import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from db import init_db
from etl import insert_cars, load_all_cars
from scrapers.cargurus_scraper import scrape_cargurus

init_db()

def main():
    st.title("CarClarity Lite 🚗")

    # Scraping control
    st.sidebar.header("Data Controls")
    if st.sidebar.button("Scrape CarGurus (once today)"):
        url = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=d586&zip=01721"
        st.sidebar.write("Scraping CarGurus... please wait ~10s")
        cars = scrape_cargurus(url, max_listings=30)
        insert_cars(cars, source="cargurus")
        st.sidebar.success(f"Inserted {len(cars)} new cars into DB")

    df = load_all_cars()

    if df is None or df.empty:
        st.warning("No cars in database. Click 'Scrape CarGurus' to add some.")
        return
    
    if df["year"].dropna().empty:
        st.warning("No valid car data in DB. Probably hit a captcha wall. Try again later or switch to a different source.")
        return

    # Filters
    year_min, year_max = int(df["year"].min()), int(df["year"].max())
    year_range = st.sidebar.slider("Year Range", min_value=year_min, max_value=year_max, value=(year_min, year_max))
    price_filter = st.sidebar.checkbox("Filter by price under $20k")
    
    filtered = df[(df["year"].astype(int) >= year_range[0]) & (df["year"].astype(int) <= year_range[1])]
    if price_filter:
        filtered = filtered[filtered["price"].str.replace("$","").str.replace(",","").astype(float) < 20000]

    st.subheader("Filtered Cars")
    st.dataframe(filtered)

    # Price histogram
    fig, ax = plt.subplots()
    prices = filtered["price"].str.replace("$","").str.replace(",","").astype(float)
    ax.hist(prices, bins=20)
    ax.set_xlabel("Price ($)")
    ax.set_ylabel("Count")
    st.pyplot(fig)

if __name__ == "__main__":
    main()