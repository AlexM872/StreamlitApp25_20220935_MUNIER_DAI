# sections/overview.py
import streamlit as st
import pandas as pd
from utils.viz import plot_kpis_by_gender, plot_mortality_over_time

def display_overview(df: pd.DataFrame):
    st.header("Overview of Mortality in France (2020-2022, COVID Period)")
    
    # KPIs en premier
    plot_kpis_by_gender(df)
    st.markdown("---")
    
    plot_mortality_over_time(df)
    st.info("This dashboard analyzes mortality in France during the COVID-19 period (2020-2022). You can observe the impact of pandemic waves and seasonal effects on death counts.\nEspecially in winter, probably also due to flu season.")