from pathlib import Path
import pandas as pd
import streamlit as st
import os

# merge_data(), merge all CSVs in one file to simplify loading
def merge_data():
    base_path = Path(__file__).resolve().parent
    data_path = base_path.parent / "data"
    output_csv = data_path / "Deces_merged.csv"

    csv_files = [f for f in data_path.glob("*.csv") if f.name != "Deces_merged.csv" and f.name != "Deces_cleaned.csv"]
    print(f"Files to merge ({len(csv_files)}): {[f.name for f in csv_files]}")

    chunks = []
    for i, csv_file in enumerate(csv_files, 1):
        print(f"Reading file {i}/{len(csv_files)}: {csv_file.name}")
        for chunk in pd.read_csv(csv_file, sep=';', low_memory=False, chunksize=200_000):
            chunks.append(chunk)
        print(f"File {csv_file.name} loaded")

    df_concat = pd.concat(chunks, ignore_index=True)
    print(f"Merge finished — {len(df_concat):,} total rows")

    df_concat.to_csv(output_csv, sep=';', index=False)
    print(f"Data saved :\n - {output_csv}")


# load_data_prep(), load the merged CSV for cleaning/preparation
def load_data_prep():
    base_path = Path(__file__).resolve().parent
    data_path = base_path.parent / "data"
    csv_path = data_path / "Deces_merged.csv"

    if csv_path.exists():
        print(f"Loading from {csv_path}")
        return pd.read_csv(csv_path, sep=';', low_memory=False)
    else:
        raise FileNotFoundError("No merged file found. Run merge_data() first.")


# load_data(), load the cleaned data (CSV or Parquet)
@st.cache_data
def load_data():
    base_path = Path(__file__).resolve().parent
    data_path = base_path.parent / "data"
    parquet_path = data_path / "Deces_cleaned.parquet"
    csv_path = data_path / "Deces_cleaned.csv"

    if parquet_path.exists():
        print(f"Loading from {parquet_path}")
        df = pd.read_parquet(parquet_path)
    elif csv_path.exists():
        print(f"Loading from {csv_path}")
        df = pd.read_csv(csv_path, sep=';', low_memory=False)
        # Conversion automatique pour la prochaine fois
        print("Convert to Parquet for future loads...")
        df.to_parquet(parquet_path, index=False)
    else:
        raise FileNotFoundError("No Deces_cleaned.csv or .parquet file found.")

    return df


# Merging all CSVs when this script is run directly
if __name__ == "__main__":
    merge_data()  # Merge all CSVs
