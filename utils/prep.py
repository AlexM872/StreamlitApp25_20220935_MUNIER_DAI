import pandas as pd
from pathlib import Path

def cleaning():
    base_path = Path(__file__).resolve().parent.parent
    data_path = base_path / "data"
    # Only use 2020–2022 CSVs
    csv_files = [data_path / f"Deces_{year}.csv" for year in [2020, 2021, 2022] if (data_path / f"Deces_{year}.csv").exists()]
    if not csv_files:
        raise FileNotFoundError("No 2020–2022 CSV files found in data directory.")
    chunks = []
    for csv_file in csv_files:
        print(f"Reading {csv_file.name}")
        for chunk in pd.read_csv(csv_file, sep=';', low_memory=False, chunksize=200_000):
            chunks.append(chunk)
    df = pd.concat(chunks, ignore_index=True)
    print(f"Loaded {len(df):,} rows from 2020–2022 CSVs.")

    # Basic diagnostics
    print('NA counts:')
    print(df.isna().sum())
    print('\nDtypes:')
    print(df.dtypes)
    print('\nDescribe (sample):')
    print(df.describe())
    print('\nInfo:')
    print(df.info())
    # Check for duplicates
    print('\nDuplicates:')
    print(df.duplicated().sum())

    # drop duplicates
    df = df.drop_duplicates()

    # drop useless column
    df = df.drop(columns=['actedeces', 'paysnaiss'], errors='ignore')

    # drop na
    df = df.dropna(subset=['lieunaiss', 'lieudeces'])
    # Basic diagnostics after initial cleaning    
    print('NA counts:')
    print(df.isna().sum())
    print(f"\nData shape after dropping duplicates and NAs: {df.shape}")
    # split nomprenom into nom and prenom if present
    if 'nomprenom' in df.columns:
        df[['nom', 'prenom']] = df['nomprenom'].astype(str).str.split('*', n=1, expand=True)
        # remove trailing slash from prenom if present
        if 'prenom' in df.columns:
            df['prenom'] = df['prenom'].astype(str).str.rstrip('/')
        print('\nSplit nom/prenom sample:')
        print(df[['nom', 'prenom']].head())

        # Remove the original nomprenom column
        df.drop(columns=['nomprenom'], inplace=True, errors='ignore')

    # transform date fields to datetime if present
    date_cols = ['datedeces', 'datenaiss']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col].astype(str), format='%Y%m%d', errors='coerce')
    
    # Drop rows where date parsing failed
    print(df.isna().sum())
    df.dropna(subset=['datedeces', 'datenaiss'], inplace=True)
    if date_cols:
        print('\nParsed date columns sample:')
        print(df[date_cols].head())
    
    # Calculate age and filter unrealistic ages
    print(df.info())
    df['age'] = ((df['datedeces'] - df['datenaiss']).dt.days / 365.25).astype(int)
    df = df[(df['age'] >= 0) & (df['age'] <= 122)]

    # Check for age variations
    print('\nAge variations:')
    print(df['age'].unique())

    # Check for shape after age filtering
    print(f"\nData shape after removing unrealistic ages: {df.shape}")

    # Extract year and month from dates
    df['annee_deces'] = df['datedeces'].dt.year
    df['mois_deces'] = df['datedeces'].dt.to_period('M').astype(str)
    df['annee_naiss'] = df['datenaiss'].dt.year
    df['mois_naiss'] = df['datenaiss'].dt.to_period('M').astype(str)
    # Map sexe to categorical
    df['sexeCategorical'] = df['sexe'].map({1: 'Male', 2: 'Female'})
    # Only keep deaths from 2020 to 2022 (COVID period)
    df = df[(df['annee_deces'] >= 2020) & (df['annee_deces'] <= 2022)]
    print('Shape after filtering to 2020–2022 (COVID period):')
    print(df.shape)
    # Save only as Parquet
    output_path_parquet = Path(__file__).resolve().parent.parent / "data" / "Deces_cleaned.parquet"
    df.to_parquet(output_path_parquet, index=False)
    print(f"Cleaned data saved in {output_path_parquet}")
    print(df.head())

if __name__ == '__main__':
	cleaning()