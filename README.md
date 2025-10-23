# 📊 Deaths in France Analysis (2010-2024)

An interactive Streamlit dashboard analyzing mortality data in France from 2010 to 2024, with insights into demographic trends, health crises impacts, and geographic patterns.

## 🎯 Overview

This project provides a comprehensive analysis of over 9 million death records from INSEE (Institut national de la statistique et des études économiques), exploring:

- **Temporal trends**: Evolution of mortality over 15 years
- **COVID-19 impact**: Excess mortality analysis and age-specific effects
- **Demographics**: Age distribution, gender differences, and generational patterns
- **Geographic insights**: Interactive map showing deaths by French department
- **Cultural analysis**: First name trends

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download this repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```



3. **Data Loading Workflow**

   When you start the app, Streamlit will attempt to load the data in one of two ways:

   - **Remote Parquet file**
     - If a `.env` file exists in the project root and contains a `DRIVE_URL` variable (e.g., a Dropbox direct download link to the Parquet file), the app will download and load the data from this remote file.

   - **Local merge and cleaning (fallback):**
     - If `DRIVE_URL` is not set or the remote file cannot be loaded, the app will automatically merge all raw CSV files in the `data/` folder, clean and process the data, and generate the cleaned files (`Deces_cleaned.csv` and `Deces_cleaned.parquet`).
     - This ensures the app works even if no remote file is available.

   The data preparation and loading process is **cached** using Streamlit's `@st.cache_data` decorator, so it only runs once per session (or when the source files change).

  **You do not need to run any manual data preparation steps.**

  If you prefer to run the steps manually:
  ```bash
  # Merge raw data files
  python -c "from utils.io import merge_data; merge_data()"

  # Clean and prepare data
  python -c "from utils.prep import cleaning; cleaning()"
  ```

4. **Run the dashboard**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 📁 Project Structure

```
project/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── data/                       # Data directory
│   ├── Deces_2010.csv         # Raw data files (2010-2024)
│   ├── ...
│   ├── Deces_merged.csv       # Merged raw data
│   └── Deces_cleaned.parquet  # Cleaned, optimized data
│
├── sections/                   # Dashboard sections
│   ├── intro.py               # Introduction & data quality overview
│   ├── overview.py            # KPIs and high-level trends
│   ├── deep_dives.py          # Detailed analyses & visualizations
│   └── conclusion.py          # Insights and limitations
│
├── utils/                      # Utility modules
│   ├── io.py                  # Data loading functions (with caching)
│   ├── prep.py                # Data cleaning and preparation
│   └── viz.py                 # Visualization functions (Plotly charts)
│
└── assets/                     # Static assets
```

## 🎨 Features

### Interactive Filters (Sidebar)
- **Year range**: Select specific time periods (2010-2024)
- **Gender**: Filter by Male, Female, or All
- **Age groups**: Predefined age brackets (0-19, 20-39, 40-59, 60-74, 75-89, 90+)
- **Place of birth**: Search by location name
- **First name**: Search by specific names

### Visualizations

#### 📈 Overview Section
- **KPI Metrics**: Total deaths, average age, median age, life expectancy by gender
- **Timeline**: Monthly deaths with COVID-19 wave annotations

#### 🔬 Deep Dives Section
1. **Excess Mortality Analysis**: Comparison with 2012-2019 baseline
2. **COVID-19 Age Impact**: Age-specific mortality during pandemic
3. **Generational Patterns**: Deaths by birth decade
4. **Country of Birth**: Distribution of foreign-born individuals
5. **🗺️ Geographic Map**: Interactive choropleth of deaths by French department
6. **Age Pyramid**: Gender-based age distribution at death
7. **First Name Analysis**: Popular names and age patterns

## 📊 Data Sources

**Source**: [Fichier des personnes décédées](https://www.data.gouv.fr/fr/datasets/fichier-des-personnes-decedees/) - INSEE via data.gouv.fr

**Coverage**: 2010-2024

**Records**: ~9 million death certificates

**Key Fields**:
- Personal info: Name, first name, gender, birth/death dates
- Location: Place of birth, country of birth
- Derived: Age at death, year/month of death

## 🧹 Data Cleaning Process

The data undergoes rigorous cleaning (see `utils/prep.py`):

1. **Deduplication**: Remove duplicate records
2. **Missing values**: Drop records with missing critical fields
3. **Name splitting**: Separate combined name fields
4. **Date parsing**: Convert string dates to datetime objects
5. **Age validation**: Filter unrealistic ages (< 0 or > 122 years)
6. **Gender mapping**: Convert codes to readable labels
7. **Time filtering**: Focus on 2010-2024 period
8. **Optimization**: Save as Parquet for performance

## 📦 Dependencies

```
pandas                 # Data manipulation
streamlit              # Web dashboard framework
plotly                 # Interactive visualizations
pyarrow                # Parquet file support
matplotlib             # Additional plotting
seaborn                # Statistical visualizations
requests               # HTTP requests
chardet                # Character encoding detection
```

## ⚠️ Limitations & Considerations

### Statistical Caveats
- **Raw counts vs. rates**: Death counts don't account for population size
  - Larger departments naturally have more deaths
  - Consider calculating mortality rates (per 100,000) for fair comparisons

- **Selection bias**: Only deceased individuals are included
  - Cannot infer population-level life expectancy
  - Represents "age at death" not "current life expectancy"

- **First name analysis**: Reflects name popularity over time
  - Older names appear more because their cohort is aging
  - Not a predictor of individual longevity

### Data Quality
- **Missing values**: Some fields (country of birth) are incomplete
  - `None` values typically indicate France as birth country
  
- **Encoding issues**: Some special characters may display incorrectly
  
- **Temporal lag**: Data may not include very recent deaths

## 👥 Credits

**Data**: INSEE - Institut national de la statistique et des études économiques

**GeoJSON**: [france-geojson.gregoiredavid.fr](https://france-geojson.gregoiredavid.fr)

**Framework**: [Streamlit](https://streamlit.io)

**Visualization**: [Plotly](https://plotly.com/python/)

## 📄 License

This project is for educational purposes. 

Data source license: [Licence Ouverte / Open License](https://www.etalab.gouv.fr/licence-ouverte-open-licence)

## 🤝 Contributing

This is an academic project. For questions or suggestions:
1. Review the code structure
2. Check data preparation steps in `utils/prep.py`
3. Explore visualization functions in `utils/viz.py`

---

**Built for Data Analysis & Visualization - EFREI 2025-2026**
