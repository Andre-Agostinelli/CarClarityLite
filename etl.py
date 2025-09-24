import pandas as pd
from sqlalchemy import Table, MetaData
from db import get_engine, init_db

def insert_cars(listings, source="cargurus"):
    """Insert scraped listings (list of dicts) into DB."""
    engine = get_engine()
    init_db()  # ensure table exists
    metadata = MetaData()
    metadata.reflect(bind=engine)

    cars = metadata.tables["cars"]

    # enrich listings with source
    for car in listings:
        car["source"] = source

    with engine.begin() as conn:
        conn.execute(cars.insert(), listings)

def load_all_cars():
    """Load all cars from DB into a Pandas DataFrame."""
    engine = get_engine()
    query = "SELECT * FROM cars"
    return pd.read_sql(query, engine)

def clear_cars():
    """Delete all cars from DB."""
    engine = get_engine()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    cars = metadata.tables["cars"]
    with engine.begin() as conn:
        conn.execute(cars.delete())
