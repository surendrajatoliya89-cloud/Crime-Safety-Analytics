# Microsoft Excel Data Analysis Guide
## Project: Crime Statistics & Safety Analytics System

This guide explains how to perform fast, professional Exploratory Data Analysis (EDA) on the clean dataset using **Microsoft Excel**, suitable for demonstration during your viva or project review.

---

### 1. Opening the Dataset in Excel
1. Open Microsoft Excel.
2. Click **File &rarr; Open &rarr; Browse**.
3. Navigate to: `Crime-Safety-Analytics/data/crime_data_clean.csv`.
4. Ensure all 1,000 rows and 18 columns load cleanly.
5. Save as an Excel Workbook (`.xlsx`) named `Crime_Analysis_Workbook.xlsx`.

---

### 2. Five Essential Pivot Tables to Create

#### Pivot Table 1: Crime Volume by Crime Type
- **Insert &rarr; PivotTable**.
- **Rows**: `Crime_Type`
- **Values**: `Incident_ID` (Summarize Values By: **Count**)
- **Additional Value**: Add `Incident_ID` a second time &rarr; Right Click &rarr; **Show Values As &rarr; % of Column Total**.
- **Finding**: Theft constitutes 32.0% of total incidents, followed by Vandalism (19.8%).

#### Pivot Table 2: Area vs. Severity Cross-Tabulation
- **Rows**: `Area`
- **Columns**: `Severity_Level` (`Low`, `Medium`, `High`)
- **Values**: `Count of Incident_ID`
- **Finding**: Downtown and Harbor District have the highest counts of Medium/High severity cases.

#### Pivot Table 3: Monthly Crime Trend
- **Rows**: `Month` (Sort chronologically: Jan &rarr; Dec)
- **Values**: `Count of Incident_ID`
- **Finding**: High incident volume peaks observed in March (104) and December (103).

#### Pivot Table 4: Time Category Distribution
- **Rows**: `Time_Category` (`Morning`, `Afternoon`, `Evening`, `Night`)
- **Values**: `Count of Incident_ID`
- **Finding**: Evening (353) and Night (239) account for 59.2% of total occurrences.

#### Pivot Table 5: Holiday vs. Non-Holiday Average Incidents
- **Rows**: `Holiday` (`Yes`, `No`)
- **Values**: `Average of Previous_Incidents`
- **Finding**: Public holidays show slightly elevated average local activity.

---

### 3. Creating Excel Pivot Charts
1. Select Pivot Table 1 &rarr; Click **PivotTable Analyze &rarr; PivotChart &rarr; Clustered Column**.
2. Select Pivot Table 3 &rarr; Click **PivotChart &rarr; Line with Markers**.
3. Select Pivot Table 4 &rarr; Click **PivotChart &rarr; Donut Chart**.

---

### 🎓 Excel Viva Tip
> **Professor:** *"Why did you use Excel when you already have Python?"*  
> **Answer:** *"Sir/Ma'am, Excel is industry-standard for rapid exploratory filtering, ad-hoc pivot tables, and sharing structured summaries with non-technical business stakeholders without needing code execution."*
