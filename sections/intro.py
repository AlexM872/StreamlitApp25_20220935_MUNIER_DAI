import streamlit as st
import pandas as pd

def display_intro(df: pd.DataFrame):
    st.title("📊 Deaths in France Analysis from 2010 to 2024")
    st.markdown("Alexandre MUNIER | alexandre.munier@efrei.net | [GitHub](https://github.com/AlexM872)")
    st.caption("Source : Fichier des personnes décédées (INSEE via data.gouv.fr)")
    st.markdown("EFREI Data Visualization Project - October 2025")
    st.header("🔍 Impact of COVID-19 on mortality and try to see correlations with different factors")
    st.header("How We Cleaned the Data: A Behind-the-Scenes Tour")
    st.markdown("""
    Before diving into the analysis, let's take a look at how we transformed raw, messy records into a reliable dataset.  

    ### Step-by-step Cleaning

    1. **Duplicate & Missing Value Removal**  
       We started by sweeping away duplicate entries and rows missing key info. This ensures each person is counted once and every record is meaningful.

    2. **Splitting Names**  
       Some records had names squished together (e.g., `DUPONT*JEAN`). We split these into separate `nom` and `prenom` columns, making it easier to analyze demographics.

    3. **Date Standardization**  
       Dates came in as strings like `20180512`. We converted these to proper date objects, for a good time-based analysis.

    4. **Age Calculation & Filtering**  
       By subtracting birth from death dates, we calculated age at death. We filtered out unrealistic ages (e.g., negative or over 122 years), keeping the data credible.

    5. **Year & Month Extraction**  
       For deeper insights, we extracted year and month from both birth and death dates, enabling seasonal and yearly trends.

    6. **Gender Mapping**  
       Gender codes (`1` for male, `2` for female) were mapped to readable labels, making charts and stats more intuitive.

    7. **Year Filtering**  
       Only deaths from 2010 onward were kept, focusing the analysis on recent trends.

    8. **Saving Clean Data**  
       The final, polished dataset was saved in both CSV and Parquet formats for fast, flexible access.

    ---
    Each step was carefully designed to turn raw data into a trustworthy foundation for analysis.  
    Here's a sample of the cleaned dataset:
    """)
    st.subheader("Sample of Cleaned Dataset")
    st.dataframe(df.head())
    st.markdown("Here, you can also see that `paysnaiss` has `None` values for many records, indicating that the country of birth is France. But, I decided to keep this column for analysis of foreign-born individuals later on.")