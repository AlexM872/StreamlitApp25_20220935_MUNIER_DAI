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
        1.  **COVID-19 Impact:** The analysis confirms significant demographic impact from the COVID-19 pandemic in France during 2020-2022, with clear mortality peaks corresponding to pandemic waves (especially the first one).

        2.  **Demographic Disparities:** The gender analysis highlights a persistent gap in life expectancy, with women living on average longer than men, even during the COVID period.

        3.  **Generational and Geographic Patterns:** Older generations and more populated regions (e.g., Île-de-France) are more represented in death counts, reflecting both demographic structure and pandemic impact.

        4.  **First Name Analysis:** Patterns in first name statistics reflect generational popularity and natality deaths, not direct links to mortality risk.

        Continued monitoring is essential to understand the long-term demographic effects of COVID-19. Careful analysis of deaths data provides valuable insights for public health and preparedness.
        For further analysis we may need data on population and deaths for years before 2020.
        """
    )