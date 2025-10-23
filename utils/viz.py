import streamlit as st
import plotly.express as px
import pandas as pd


# basic KPIS in overview
def plot_kpis_by_gender(df: pd.DataFrame):
    """Show basic KPIs, respecting the gender filter."""
    total_deces = len(df)
    age_moyen = int(df['age'].mean()) if not df.empty else 0
    age_median = int(df['age'].median()) if not df.empty else 0
    
    life_exp = df.groupby('sexeCategorical')['age'].mean().round(1).to_dict()
    age_homme = life_exp.get('Male', 'N/A')
    age_femme = life_exp.get('Female', 'N/A')

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total deaths", f"{total_deces:,}".replace(',', ' '))
    c2.metric("Average age", f"{age_moyen} years")
    c3.metric("Median age", f"{age_median} years")
    c4.metric("Average age Female/Male", f"{age_femme} / {age_homme} years")

# age distribution by gender
def plot_age_distribution_by_gender(df: pd.DataFrame):
    """Show histogram of age distribution by gender"""
    st.subheader("Deaths by Age and Gender")
    fig = px.histogram(
        df, x='age', color='sexeCategorical', barmode='overlay', nbins=100,
        title="Distribution of Age at Death by Gender",
        labels={'age': 'Age', 'sexeCategorical': 'Gender'},
        color_discrete_map={'Male': 'royalblue', 'Female': 'pink'}
    )
    fig.update_traces(opacity=0.7)
    st.plotly_chart(fig, use_container_width=True)

def plot_mortality_over_time(df: pd.DataFrame):
    """Show evolution of mortality with detailed COVID waves (2020-2022 only)."""
    # Daily deaths for more granular COVID impact analysis
    daily_deaths = df.groupby('datedeces').size().reset_index(name='count')
    fig = px.line(
        daily_deaths,
        x='datedeces',
        y='count',
        title="Daily Deaths in France (2020-2022)",
        labels={'datedeces': 'Date of Death', 'count': 'Number of Deaths'}
    )

    # Highlight major COVID waves (approximate dates)
    fig.add_vrect(x0="2020-03-15", x1="2020-05-15", fillcolor="#FFADAD", opacity=0.3, line_width=0, annotation_text="1st Wave")
    fig.add_vrect(x0="2020-10-15", x1="2021-01-15", fillcolor="#FFADAD", opacity=0.3, line_width=0, annotation_text="2nd Wave")
    fig.add_vrect(x0="2021-08-01", x1="2021-10-01", fillcolor="#FFADAD", opacity=0.3, line_width=0, annotation_text="3rd Wave (Delta)")

    st.plotly_chart(fig, use_container_width=True)

def plot_excess_mortality(df: pd.DataFrame):
    """Calculate and show monthly excess mortality for the COVID period (2020-2022)."""
    # Use average monthly deaths from Ined (2015-2019): 50,048
    # Source: Institut national d'études démographiques (Ined)
    st.warning("Warning: This chart is irrelevant if filters are applied, because the monthly average is constant.")
    st.info("The average number of deaths per month in France between 2015 and 2019 was approximately 50,048. This was calculated by summing annual deaths from Ined and dividing by 60 months.\n\nAnnual deaths: 2015: 593,680 | 2016: 593,865 | 2017: 606,274 | 2018: 609,648 | 2019: 599,408.\n\nSource: Institut national d'études démographiques (Ined), https://www.ined.fr/en/everything_about_population/data/france/mortality-deaths/number-deaths/.")

    covid_df = df[df['annee_deces'] >= 2020].copy()
    covid_monthly = covid_df.groupby('mois_deces').size().reset_index(name='deces_2020_plus')
    covid_monthly['mois'] = pd.to_datetime(covid_monthly['mois_deces']).dt.month

    # Create baseline DataFrame
    baseline_monthly = pd.DataFrame({
        'mois': list(range(1, 13)),
        'baseline_avg': [50048] * 12
    })

    comparison_df = pd.merge(covid_monthly, baseline_monthly, on='mois', how='left')
    comparison_df['surmortalite'] = comparison_df['deces_2020_plus'] - comparison_df['baseline_avg']

    fig = px.bar(comparison_df, x='mois_deces', y='surmortalite',
                 title="Excess Mortality Compared to 2015-2019 Monthly Average (Source: Ined)",
                 labels={'mois_deces': 'Months', 'surmortalite': 'Excess Deaths'})
    fig.update_traces(marker_color=['red' if val > 0 else 'green' for val in comparison_df['surmortalite']])
    st.plotly_chart(fig, use_container_width=True)

def plot_deaths_by_generation(df: pd.DataFrame):
    """Analyze mortality by decade of birth."""
    st.subheader("Mortality by Generation")
    if df.empty:
        st.info("Not enough data to display the generation analysis with the current filters.")
        return
    df_gen = df.copy()
    df_gen['generation'] = (df_gen['annee_naiss'] // 10) * 10
    generation_counts = df_gen['generation'].value_counts().sort_index()
    fig = px.bar(generation_counts, x=generation_counts.index, y=generation_counts.values,
                 title="Number of Deaths by Birth Decade",
                 labels={'x': 'Birth Decade', 'y': 'Number of Deaths'})
    st.plotly_chart(fig, use_container_width=True)

def plot_prenom_analysis(df: pd.DataFrame):
    """Analyze names, with handling for cases where there is little data."""
    st.markdown("---")
    st.subheader("Is Name related to Age at Death ?")
    st.warning("Warning: These graphs are statistical curiosities and should not be over-interpreted.")

    min_count = 500
    prenom_counts = df['prenom'].value_counts()
    common_prenoms = prenom_counts[prenom_counts >= min_count].index
    df_filtered = df[df['prenom'].isin(common_prenoms)]
    # If after filtering by popularity, there is no more data, we stop.
    if df_filtered.empty:
        st.info("Not enough data to display the name analysis with the current filters. Try with a broader selection.")
        return

    col1, col2 = st.columns(2)
    with col1:
        top_prenoms = df_filtered['prenom'].value_counts().nlargest(15).sort_values(ascending=True)
        fig = px.bar(top_prenoms, x=top_prenoms.values, y=top_prenoms.index, orientation='h', title="Top 15 Most Common Names", labels={'x': 'Number of Deaths', 'y': 'First Name'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        avg_age_by_prenom = df_filtered.groupby('prenom')['age'].mean().nsmallest(15).sort_values(ascending=False)
        fig = px.bar(avg_age_by_prenom, x=avg_age_by_prenom.values, y=avg_age_by_prenom.index, orientation='h',
                      title="Top 15 Names by Average Age at Death (Lowest)", labels={'x': 'Average Age at Death', 'y': 'First Name'})
        st.plotly_chart(fig, use_container_width=True)

def plot_covid_age_impact(df: pd.DataFrame):
    """
    Shows the age distribution of deaths for each major COVID wave (2020-2022 only).
    Reveals which age groups were most affected during each wave using only available data.
    """
    st.info("This chart shows the age distribution of deaths for each major COVID wave in France (2020-2022). It highlights which age groups were most affected during each wave, using only available data.")
    # Define wave periods (approximate)
    wave_periods = {
        '1st Wave (Spring 2020)': ('2020-03-15', '2020-05-15'),
        '2nd Wave (Winter 2020-21)': ('2020-10-15', '2021-01-15'),
        '3rd Wave (Delta, Summer 2021)': ('2021-08-01', '2021-10-01'),
        'Other (Rest of 2020-2022)': None
    }

    age_distributions = {}
    for wave, period in wave_periods.items():
        if period is not None:
            start, end = period
            mask = (df['datedeces'] >= pd.to_datetime(start)) & (df['datedeces'] <= pd.to_datetime(end))
            age_distributions[wave] = df.loc[mask, 'age'].value_counts().sort_index()
        else:
            # All other dates not in defined waves
            mask = ~(
                ((df['datedeces'] >= pd.to_datetime('2020-03-15')) & (df['datedeces'] <= pd.to_datetime('2020-05-15')))
                | ((df['datedeces'] >= pd.to_datetime('2020-10-15')) & (df['datedeces'] <= pd.to_datetime('2021-01-15')))
                | ((df['datedeces'] >= pd.to_datetime('2021-08-01')) & (df['datedeces'] <= pd.to_datetime('2021-10-01')))
            )
            age_distributions[wave] = df.loc[mask, 'age'].value_counts().sort_index()

    # Prepare data for plotting
    plot_df = pd.DataFrame()
    for wave, dist in age_distributions.items():
        temp = pd.DataFrame({'age': dist.index, 'deaths': dist.values, 'wave': wave})
        plot_df = pd.concat([plot_df, temp], ignore_index=True)

    # Plot
    fig = px.line(
        plot_df,
        x='age',
        y='deaths',
        color='wave',
        title="Age Distribution of Deaths by COVID Wave (2020-2022)",
        labels={'age': 'Age at Death', 'deaths': 'Number of Deaths', 'wave': 'COVID Wave'}
    )
    fig.update_layout(xaxis_title='Age at Death', yaxis_title='Number of Deaths')
    st.plotly_chart(fig, use_container_width=True)

def plot_deaths_by_department_map(df: pd.DataFrame):
    """
    Displays a choropleth map of France showing deaths by department.
    Uses the first 2 digits of lieudeces code to determine department.
    """
    st.subheader(" Geographic Distribution: Deaths by Department of Death")
    
    # Extract department code from lieudeces (first 2 digits)
    df_map = df.copy()
    df_map['dept_code'] = df_map['lieudeces'].astype(str).str[:2]
    
    # Filter out invalid department codes (only keep 01-95 and 2A, 2B for Corsica)
    valid_depts = [f"{i:02d}" for i in range(1, 96)]
    df_map = df_map[df_map['dept_code'].isin(valid_depts)]
    
    # Count deaths by department
    dept_counts = df_map['dept_code'].value_counts().reset_index()
    dept_counts.columns = ['dept_code', 'deaths']
    
    # Add department names (simplified mapping for major departments)
    dept_names = {
        '01': 'Ain', '02': 'Aisne', '03': 'Allier', '04': 'Alpes-de-Haute-Provence',
        '05': 'Hautes-Alpes', '06': 'Alpes-Maritimes', '07': 'Ardèche', '08': 'Ardennes',
        '09': 'Ariège', '10': 'Aube', '11': 'Aude', '12': 'Aveyron', '13': 'Bouches-du-Rhône',
        '14': 'Calvados', '15': 'Cantal', '16': 'Charente', '17': 'Charente-Maritime',
        '18': 'Cher', '19': 'Corrèze', '21': 'Côte-d\'Or', '22': 'Côtes-d\'Armor',
        '23': 'Creuse', '24': 'Dordogne', '25': 'Doubs', '26': 'Drôme', '27': 'Eure',
        '28': 'Eure-et-Loir', '29': 'Finistère', '30': 'Gard', '31': 'Haute-Garonne',
        '32': 'Gers', '33': 'Gironde', '34': 'Hérault', '35': 'Ille-et-Vilaine',
        '36': 'Indre', '37': 'Indre-et-Loire', '38': 'Isère', '39': 'Jura', '40': 'Landes',
        '41': 'Loir-et-Cher', '42': 'Loire', '43': 'Haute-Loire', '44': 'Loire-Atlantique',
        '45': 'Loiret', '46': 'Lot', '47': 'Lot-et-Garonne', '48': 'Lozère', '49': 'Maine-et-Loire',
        '50': 'Manche', '51': 'Marne', '52': 'Haute-Marne', '53': 'Mayenne', '54': 'Meurthe-et-Moselle',
        '55': 'Meuse', '56': 'Morbihan', '57': 'Moselle', '58': 'Nièvre', '59': 'Nord',
        '60': 'Oise', '61': 'Orne', '62': 'Pas-de-Calais', '63': 'Puy-de-Dôme',
        '64': 'Pyrénées-Atlantiques', '65': 'Hautes-Pyrénées', '66': 'Pyrénées-Orientales',
        '67': 'Bas-Rhin', '68': 'Haut-Rhin', '69': 'Rhône', '70': 'Haute-Saône',
        '71': 'Saône-et-Loire', '72': 'Sarthe', '73': 'Savoie', '74': 'Haute-Savoie',
        '75': 'Paris', '76': 'Seine-Maritime', '77': 'Seine-et-Marne', '78': 'Yvelines',
        '79': 'Deux-Sèvres', '80': 'Somme', '81': 'Tarn', '82': 'Tarn-et-Garonne',
        '83': 'Var', '84': 'Vaucluse', '85': 'Vendée', '86': 'Vienne', '87': 'Haute-Vienne',
        '88': 'Vosges', '89': 'Yonne', '90': 'Territoire de Belfort', '91': 'Essonne',
        '92': 'Hauts-de-Seine', '93': 'Seine-Saint-Denis', '94': 'Val-de-Marne', '95': 'Val-d\'Oise'
    }
    
    dept_counts['dept_name'] = dept_counts['dept_code'].map(dept_names).fillna(dept_counts['dept_code'])
    
    # Create choropleth map using Plotly's built-in France geometry
    fig = px.choropleth(
        dept_counts,
        locations='dept_code',
        geojson='https://france-geojson.gregoiredavid.fr/repo/departements.geojson',
        featureidkey='properties.code',
        color='deaths',
        hover_name='dept_name',
        hover_data={'dept_code': True, 'deaths': ':,'},
        color_continuous_scale='YlOrRd',
        labels={'deaths': 'Number of Deaths'},
        title='Deaths by Department of Death (2020-2022)'
    )
    
    # Update map layout to focus on France
    fig.update_geos(
        fitbounds="locations",
        visible=False
    )
    
    fig.update_layout(
        height=600,
        margin={"r": 0, "t": 30, "l": 0, "b": 0}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show top 10 departments
    st.markdown("**Top 10 Departments by Number of Deaths:**")
    top_10 = dept_counts.nlargest(10, 'deaths')[['dept_code', 'dept_name', 'deaths']]
    top_10['deaths'] = top_10['deaths'].apply(lambda x: f"{x:,}")
    st.dataframe(top_10, hide_index=True, use_container_width=True)
