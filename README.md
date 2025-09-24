# CarClarityLite
Used car shopping tool
1. python -m venv .venv && source .venv/Scripts/activate <!-- depends on path/OS -->
2. pip install -r requirements.txt
3. Run python etl.py to insert into DB.
4. Run streamlit run app.py to view data & tweak filters.
5. When scrapers work reliably, run python deal_algo.py to compute deal scores, then see them in Streamlit.