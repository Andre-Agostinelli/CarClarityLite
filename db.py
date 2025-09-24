from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

DB_FILE = "cars.db"

def get_engine():
    return create_engine(f"sqlite:///{DB_FILE}", echo=False, future=True)

def init_db():
    engine = get_engine()
    metadata = MetaData()

    cars = Table(
        "cars",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("title", String),
        Column("price", String),
        Column("year", String),
        Column("make", String),
        Column("model", String),
        Column("trim", String),
        Column("mileage", String),
        Column("body", String),
        Column("fuel", String),
        Column("mpg", String),
        Column("color", String),
        Column("source", String),   # new
    )

    metadata.create_all(engine)
    return engine