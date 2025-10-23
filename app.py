# app.py
import streamlit as st
from utils.io import load_data
from utils.prep import cleaning
st.set_page_config(page_title="Deaths in France Analysis", layout="wide")

st.set_page_config(page_title="Deaths in France Analysis", layout="wide")

from sections.intro import display_intro
from sections.overview import display_overview
from sections.deep_dives import display_deep_dives
from sections.conclusion import display_conclusion

def prepare_and_load_data():
    import os
    from pathlib import Path
    parquet_path = Path(__file__).resolve().parent / "data" / "Deces_cleaned.parquet"
    if parquet_path.exists():
        return load_data()
    else:
        cleaning()
        return load_data()

df = prepare_and_load_data()

# Sidebar with filters
st.sidebar.header("Filters")

# Year filter
min_year, max_year = 2020, 2022
min_age, max_age = int(df['age'].min()), int(df['age'].max())

# Sex filter
sex_options = ['All'] + df['sexeCategorical'].unique().tolist()
selected_sex = st.sidebar.selectbox("Sex", sex_options)

# Filter by place of birth
commune_input = st.sidebar.text_input("Search for a place of birth")
# Filter by first name
prenom_input = st.sidebar.text_input("Search for a first name")
# Check a box for exclusive first name filtering
exclusive_prenom = st.sidebar.checkbox("Exclusive first name filtering")
# Filter by year of birth
min_birth_year, max_birth_year = int(df['annee_naiss'].min()), int(df['annee_naiss'].max())

age_group_options = {
    'All': (min_age, max_age),
    '90 and more': (90, max_age),
    '75-89': (75, 89),
    '60-74': (60, 74),
    '40-59': (40, 59),
    '20-39': (20, 39),
    '20 and less': (0, 19)
}
selected_age_group = st.sidebar.selectbox("Age Group", list(age_group_options.keys()))
age_range = age_group_options[selected_age_group]

# Filters
df_filtered = df[(df['annee_deces'] >= 2020) & (df['annee_deces'] <= 2022)]

if selected_sex != 'All':
    df_filtered = df_filtered[df_filtered['sexeCategorical'] == selected_sex]

# Apply place of birth filter if user entered text
if commune_input:
    df_filtered = df_filtered[df_filtered['commnaiss'].str.contains(commune_input, case=False, na=False)]
# Apply first name filter if user entered text
if prenom_input and not exclusive_prenom:
    df_filtered = df_filtered[df_filtered['prenom'].str.contains(prenom_input, case=False, na=False)]
    # Display the list of matching first names
    matching_prenoms = df[df['prenom'].str.contains(prenom_input, case=False, na=False)]['prenom'].unique()
    st.sidebar.write("Matching first names:", matching_prenoms)
elif prenom_input and exclusive_prenom:
    #Only take people with this exact first name
    df_filtered = df_filtered[df_filtered['prenom'] == str.upper(prenom_input)]

if selected_age_group != 'All':
    df_filtered = df_filtered[
        (df_filtered['age'] >= age_range[0]) & (df_filtered['age'] <= age_range[1])
    ]

# --- Sections ---
display_intro(df)
display_overview(df_filtered)
display_deep_dives(df_filtered)
display_conclusion()