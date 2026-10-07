# Crime Statistics & Safety Analytics System Using Data Science and Machine Learning
### B.Sc Data Science Final Project &bull; CrimeWatch Analytics

---

## 1. Project Title & Branding
**CrimeWatch Analytics** &mdash; Crime Statistics & Safety Analytics System Using Data Science and Machine Learning.

---

## 2. Project Overview
CrimeWatch Analytics is an end-to-end Data Science and Machine Learning web application built as a flagship first portfolio project for B.Sc Data Science students. The system ingests historical incident data, performs automated data cleaning and Exploratory Data Analysis (EDA), trains an ensemble Machine Learning model (**Random Forest Classifier**) to estimate scenario risk tiers, and presents dynamic visual statistics and data-driven safety insights through a clean, professional web application.

---

## 3. Problem Statement
Municipalities and safety planners generate extensive historical crime logs, but this data is frequently siloed in raw tables and inaccessible to decision-makers. Furthermore, many commercial predictive policing tools rely on intrusive surveillance or opaque individual profiling. 

There is a critical need for an **educational, ethical, and interpretable** analytical system that focuses strictly on aggregate historical patterns, descriptive metrics, and pre-incident contextual risk assessment without invading individual civil liberties.

---

## 4. Key Objectives
- Analyze historical crime statistics to identify high-volume incident types and geographic areas.
- Explore temporal patterns across months, days of the week, and times of day.
- Perform robust data preprocessing (deduplication, median/mode imputation, datetime parsing).
- Train an interpretable Random Forest Classifier pipeline achieving &ge; 85% accuracy.
- Build an intuitive web application with 5 live KPI cards and Chart.js visualizations.
- Provide relational data access through MySQL queries and an automated fail-safe database layer.
- Integrate business intelligence reporting through Microsoft Excel and Microsoft Power BI.

---

## 5. Dataset Architecture
The project utilizes a curated educational historical dataset located at `data/crime_data_clean.csv` comprising 1,000 incident records with 18 features:
- **Incident Identifiers**: `Incident_ID`, `Date`, `Year`, `Month`, `Day_of_Week`, `Time_Category`
- **Location Attributes**: `City`, `Area`, `Location_Type`
- **Incident Attributes**: `Crime_Type`, `Crime_Category`, `Severity_Level`
- **Contextual Factors**: `Victim_Age`, `Victim_Gender`, `Weather`, `Holiday`, `Previous_Incidents`
- **Target Label**: `Crime_Risk_Level` (`Low`, `Medium`, `High`)

---

## 6. Data Cleaning (`clean_data.py`)
Data quality operations performed using Pandas:
- **Deduplication**: Identifies and drops duplicate incident entries based on `Incident_ID`.
- **Numerical Imputation**: Missing values in `Victim_Age` imputed using the **median** (resistant to outliers).
- **Categorical Imputation**: Missing values in `Weather` and `Location_Type` imputed using the **mode**.
- **Type Standardization**: Parsed dates into standard datetime objects and stripped leading/trailing whitespaces.

---

## 7. Exploratory Data Analysis (`analysis.py`)
Core findings from historical data analysis:
- **Dominant Crime Type**: Theft accounts for 32.0% of total reported incidents, followed by Vandalism (19.8%) and Burglary (18.0%).
- **Severity Ratio**: 62.4% Low Severity, 28.7% Medium Severity, and 8.9% High Severity.
- **Time Dynamics**: Evening (35.3%) and Night (23.9%) account for over 59% of reported cases.
- **Geographic Concentration**: Downtown and Harbor District exhibit the highest volume of reported incidents.

---

## 8. Machine Learning Pipeline (`train_model.py`)
- **Model Type**: Random Forest Classifier (`n_estimators=100`, `max_depth=12`, `random_state=42`).
- **Feature Selection (No Target Leakage)**: `Area`, `Crime_Type`, `Month`, `Day_of_Week`, `Time_Category`, `Weather`, `Holiday`, `Location_Type`, and `Previous_Incidents`.
- **Scikit-learn Pipeline**: Bundles `ColumnTransformer` (OneHotEncoder + StandardScaler) with the classifier to guarantee consistent preprocessing during both training and live inference.

---

## 9. Model Evaluation
- **Accuracy**: 87.00%
- **Precision**: 86.93%
- **Recall**: 87.00%
- **F1 Score**: 86.81%
- **Top Predictive Features**:
  1. `Previous_Incidents` (23.27%)
  2. `Area_Harbor District` (6.79%)
  3. `Area_Downtown` (5.52%)
  4. `Area_Industrial Park` (4.49%)
  5. `Time_Category_Afternoon` (4.27%)

---

## 10. Web Application Architecture (`app.py`)
Built using Python and Flask following MVC architecture:
- `/` &mdash; Executive Dashboard with 5 KPI cards and Chart.js charts.
- `/crimes` &mdash; Searchable, filterable, and paginated historical crime data explorer.
- `/predict` &mdash; Interactive scenario risk classification form with probabilities and explanation.
- `/analytics` &mdash; Deep-dive multi-dimensional analytics and Data-Driven Safety Insights.
- `/about` &mdash; Complete academic documentation, methodology, and ethical framework.
- `/api/charts-data` &mdash; JSON endpoint feeding dynamic data to Chart.js.

---

## 11. Database Layer (`database/database.sql`)
- Normalized MySQL schema (`crime_records`) and 10 analytical SQL queries.
- Automated fail-safe helper (`db_helper.py`) queries MySQL when available and transparently falls back to local SQLite to ensure 100% reliability during college demonstrations.

---

## 12. Microsoft Excel Reporting (`reports/EXCEL_ANALYSIS_GUIDE.md`)
Step-by-step instructions for creating 5 essential Pivot Tables, slicers, and Pivot Charts in Excel.

---

## 13. Microsoft Power BI Reporting (`reports/POWER_BI_DASHBOARD_GUIDE.md`)
Complete guide to building an executive Power BI dashboard with 5 DAX measures, KPI cards, and interactive slicers.

---

## 14. Ethical Safeguards & Anti-Surveillance Guarantee
- **No Individual Profiling**: The model predicts scenario risk categories, never individuals.
- **No Facial Recognition / CCTV Analysis**: No biometric data or video feeds are used.
- **Prominent Disclaimers**: Displayed on all pages to clarify that predictions reflect historical patterns, not certain future events.

---

## 15. Limitations
- Reflects only reported crime; unreported incidents cannot be captured.
- Educational synthetic dataset designed for academic demonstration.
- Historical models require periodic retraining to adapt to community trends.

---

## 16. Future Scope
- Ingesting official municipal open data feeds.
- Geospatial mapping with Leaflet / GeoJSON.
- Automated pipeline re-training schedules.

---

## 17. Installation & Quickstart Guide

### Prerequisites
- Python 3.10+ (Python 3.13 recommended)

### Step 1: Clone or Navigate to Project
```powershell
cd "C:\Users\Admin\OneDrive\Desktop\Crime-Safety-Analytics"
```

### Step 2: Create & Activate Virtual Environment
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Train Machine Learning Model
```powershell
python train_model.py
```

### Step 5: Start the Web Application
```powershell
python app.py
```
Open your web browser and navigate to: **`http://127.0.0.1:5000`**

---

## 18. Viva Voice Preparation
Read the full viva question-and-answer preparation guide in:  
📁 `reports/VIVA_DEFENSE_GUIDE.md`
