import pandas as pd
import sys
from pathlib import Path
from utils.io import load_data_prep


def cleaning():
	df = load_data_prep()

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

	#drop duplicates
	df = df.drop_duplicates()

	#drop useless column
	df = df.drop(columns=['actedeces', 'lieudeces'], errors='ignore')

	#drop na
	df = df.dropna(subset=['lieunaiss'])
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
	# delete rows with death years before 2010
	df = df[df['annee_deces'] >= 2010]
	print('Shape after filtering years before 2010:')
	print(df.shape)
	# Save the data
	output_path = Path(__file__).resolve().parent.parent / "data" / "Deces_cleaned.csv"
	output_path_parquet = Path(__file__).resolve().parent.parent / "data" / "Deces_cleaned.parquet"
	df.to_csv(output_path, index=False, sep=';')
	df.to_parquet(output_path_parquet, index=False)
	print(f"Cleaned data saved in {output_path}")
	print(df.head())

if __name__ == '__main__':
	cleaning()