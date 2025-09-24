# deal_algo.py
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, select
from db import Listing, get_engine
from sklearn.linear_model import LinearRegression

def compute_peer_stats(df):
    # assume df has price, mileage
    mean = df['price'].mean()
    std = df['price'].std(ddof=0) if df['price'].std(ddof=0) > 0 else 1.0
    median = df['price'].median()
    mad = (np.abs(df['price'] - median)).median() or 1.0
    return {"mean": mean, "std": std, "median": median, "mad": mad}

def deal_score_for_listing(row, peers):
    # z-score
    if pd.isna(row['price']):
        return None
    stats = compute_peer_stats(peers)
    z = (row['price'] - stats['mean']) / stats['std']
    robust_z = (row['price'] - stats['median']) / stats['mad']
    # simple combined score (lower = better deal)
    score = 0.6 * z + 0.4 * robust_z
    return float(score)

def compute_deal_scores(db_path="sqlite:///cars.db"):
    engine = get_engine(db_path)
    conn = engine.connect()
    df = pd.read_sql_table("listings", conn)
    df['deal_score'] = None
    for idx, row in df.iterrows():
        # define peer group: same make/model, year +/-1, mileage +/-5000
        peers = df[
            (df['make'] == row['make']) &
            (df['model'] == row['model']) &
            (abs(df['year'] - row['year']) <= 1) &
            (abs(df['mileage'] - row['mileage']) <= 5000)
        ]
        if len(peers) >= 5:
            df.at[idx, 'deal_score'] = deal_score_for_listing(row, peers)
        else:
            # fallback: broader peers (same make/model only)
            peers2 = df[(df['make'] == row['make']) & (df['model'] == row['model'])]
            if len(peers2) >= 5:
                df.at[idx, 'deal_score'] = deal_score_for_listing(row, peers2)
            else:
                df.at[idx, 'deal_score'] = None
    # write back to DB
    for i, r in df.iterrows():
        if r['deal_score'] is not None:
            conn.execute(
                f"UPDATE listings SET deal_score = :s WHERE id = :id",
                {"s": float(r['deal_score']), "id": int(r['id'])}
            )
    conn.close()
    return df