# sections/conclusion.py
import streamlit as st

def display_conclusion():
    st.markdown("---")
    
    # --- Section sur la Qualité des Données et les Limites ---
    st.markdown("### Quality of the Data & Limitations")
    st.info(
        """
        - **Sources :** The data originates from the INSEE database of deaths in France from 1970, accessible at data.gouv.fr.

        - **Data cleaning :** The data was pre-processed to exclude entries with invalid dates and statistically aberrant ages (<0 or >122 years).

        - **Limitations :**
            - **Bias of population :** This analysis presents raw death counts. A department or municipality with more deaths may simply be more populated. For a fairer analysis, a **mortality rate** (deaths per 100,000 inhabitants) should be calculated.
            - **First Name Analysis :** The statistics on first names are a curiosity and mainly reflect the popularity of a name at a certain time rather than any "destiny".
        """
    )

    # --- Section sur les Principaux Enseignements (Insights) ---
    st.markdown("### Learnings")
    st.success(
        """
        1.  **COVID-19 Impact :** A mortality peak in 2020, visible on the evolution curve, confirms the significant demographic impact of the COVID-19 pandemic in France. We can see that after 2020, the mortality rate seems to stabilize at a higher level than pre-pandemic years, possibly indicating lasting effects.

        2.  **Demographic Disparities :** The gender analysis highlights a consistent gap in life expectancy, with women living on average longer than men.

        3.  **Seasonal cycles :** Beyond crises, the data reveals seasonal mortality patterns, with peaks during winter months likely linked to flu epidemics. The peaks are particularly pronounced in 2017 and 2022 and totally make heatwaves effects negligible on mortality in France.

        For now, COVID-19 seems to have passed its peak impact, but continued monitoring is essential to understand its long-term demographic effects.
        Deaths data, when analyzed carefully, can provide valuable insights into public health trends and inform future preparedness strategies.
        """
    )