# sections/deep_dives.py
import streamlit as st
import pandas as pd
from utils.viz import (
    plot_excess_mortality,
    plot_age_distribution_by_gender,
    plot_deaths_by_generation,
    plot_prenom_analysis,
    plot_covid_age_impact,
    plot_deaths_by_department_map,
)

def display_deep_dives(df: pd.DataFrame):
    st.header("Deep Dives into Mortality Patterns")

    # Crisis and Demographics Focus
    st.subheader("Impact of Health Crises and Seasonality")
    st.markdown("Beyond the overall trend, mortality is marked by shocks (like pandemics) and cycles (like flu epidemics).")
    
    col1, col2 = st.columns(2)
    with col1:
        # This chart quantifies the impact seen in the overview timeline.
        st.subheader("Excess Mortality (vs mean of 2015-2019)")
        plot_excess_mortality(df)
    with col2:
        # This chart shows how COVID-19 affected different age groups.
        st.subheader("COVID-19 Impact by Age")
        plot_covid_age_impact(df)
    st.markdown("### Quick Analysis")
    st.markdown("Here, we observe that the 2020 COVID-19 pandemic led to significant excess mortality. Seasonal patterns also emerge, with higher mortality during winter months due to factors like influenza.")
    st.markdown("Also, we can see that there is, in general, a higher impact on older age groups, which is consistent with the known vulnerability of the elderly to COVID-19.")
    st.markdown("---")

    # Analyze by Generation and Origins
    col1, col2 = st.columns(2)
    with col1:
        plot_deaths_by_generation(df)
    with col2:
        plot_age_distribution_by_gender(df)
    st.markdown("### Quick Analysis")
    st.markdown("Here, we can clearly see the differences in mortality patterns across generations. The age distribution by gender also highlights the longevity gap between men and women")
    st.markdown("This chart also allows us to see that there is still around 5% of deaths right after the birth.")
    st.info("It is important to notice that natality deaths is generally around 5% because it will allow us to do good analysis on first names later on.")
    st.markdown("---")
    
    # Geographic Distribution Map
    plot_deaths_by_department_map(df)
    st.markdown("### Quick Analysis")
    st.markdown("The map shows the geographic distribution of deaths, highlighting areas with higher mortality rates.")
    st.markdown("We can see that more populated areas like Île-de-France have higher death counts, which is expected. It is also in these areas that COVID-19 had significant impacts.")
    st.markdown("---")

    # Analysis on First Names
    plot_prenom_analysis(df)
    st.markdown("### Quick Analysis")
    st.markdown("This analysis of first names didn't really show a correlation between first names and mortality rates. The patterns observed are more reflective of the popularity of certain names during specific time periods rather than any direct influence on mortality.")
    st.markdown("If the first name is quite new, we can see that the average age at death can be very low due to natality deaths.")
    st.markdown("For example:  `Thibault` is a name that became popular in the 90s, so the average age at death is at 28. In the previous charts, when we filter the deaths with first name, we can observe that the age where most of `Thibault`s die is mostly 0, corresponding to natality deaths.")
    st.markdown("But, as we know, natality deaths is most likely around 5% of total deaths. So, that means that most of the `Thibault`s are still alive.")