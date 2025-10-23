# sections/overview.py
import streamlit as st
import pandas as pd
from utils.viz import plot_kpis_by_gender, plot_mortality_over_time

def display_overview(df: pd.DataFrame):
    st.header("Vue d'ensemble de la mortalité en France")
    
    # KPIs en premier
    plot_kpis_by_gender(df)
    st.markdown("---")
    
    plot_mortality_over_time(df)
    st.info("Here, we can see a clear mortality peak in 2020, corresponding to the COVID-19 pandemic's impact in France." \
    " The trend also shows that there is peak of deaths during winter periods and especially in 2017 and 2022, probably due to flu epidemics.")