import streamlit as st
import pandas as pd

def display_intro(df: pd.DataFrame):
    st.title("📊 Deaths in France Analysis (2020-2022, COVID Period)")
    st.markdown("Alexandre MUNIER | alexandre.munier@efrei.net | [GitHub](https://github.com/AlexM872)")
    st.caption("Source : Fichier des personnes décédées (INSEE via data.gouv.fr)")
    st.markdown("EFREI Data Visualization Project - October 2025")
    st.header("🔍 Impact of COVID-19 on mortality in France (2020-2022)")
    st.header("How I Cleaned the Data: Focusing on the COVID Period (2020-2022)")
    st.markdown("""
Before diving into the analysis, let's take a look at how I transformed raw, messy records into a reliable dataset.  

### Step-by-step Cleaning

1. **Duplicate & Missing Value Removal**  
   I started by sweeping away duplicate entries and rows missing key info. This ensures each person is counted once and every record is meaningful.

2. **Splitting Names**  
   Some records had names squished together (e.g., `DUPONT*JEAN`). I split these into separate `nom` and `prenom` columns, making it easier to analyze demographics.

3. **Date Standardization**  
   Dates came in as strings like `20180512`. I converted these to proper date objects, for a good time-based analysis.

4. **Age Calculation & Filtering**  
   By subtracting birth from death dates, I calculated age at death. I filtered out unrealistic ages (e.g., negative or over 122 years), keeping the data credible.

5. **Year & Month Extraction**  
   For deeper insights, I extracted year and month from both birth and death dates, enabling seasonal and yearly trends.

6. **Gender Mapping**  
   Gender codes (`1` for male, `2` for female) were mapped to readable labels, making charts and stats more intuitive.

7. **Year Filtering**  
   Only deaths from 2020 to 2022 were kept, focusing the analysis on the COVID period.

8. **Saving Clean Data**  
   The final, polished dataset was saved in both CSV and Parquet formats for fast, flexible access.

---
    Each step was carefully designed to turn raw data into a trustworthy foundation for analysis.  
    Here's a sample of the cleaned dataset:
    """)
    st.subheader("Sample of Cleaned Dataset")
    st.dataframe(df.head())
    st.markdown("---")
    