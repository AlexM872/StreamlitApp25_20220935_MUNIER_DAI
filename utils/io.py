from pathlib import Path
import pandas as pd
import streamlit as st

# load_data(), load the cleaned data (Parquet only)
@st.cache_data
def load_data():
    base_path = Path(__file__).resolve().parent
    data_path = base_path.parent / "data"
    parquet_path = data_path / "Deces_cleaned.parquet"

    if parquet_path.exists():
        print(f"Loading from {parquet_path}")
        df = pd.read_parquet(parquet_path)
        return df
    else:
        raise FileNotFoundError("No Deces_cleaned.parquet file found.")
