# Microsoft Power BI Interactive Dashboard Guide
## Project: Crime Statistics & Safety Analytics System

This guide outlines how to build an executive presentation dashboard in **Microsoft Power BI** using `data/crime_data_clean.csv`.

---

### 1. Connecting Data in Power BI Desktop
1. Open **Power BI Desktop**.
2. Click **Get Data &rarr; Text/CSV**.
3. Select `data/crime_data_clean.csv` and click **Load**.
4. In the Data View, confirm `Date` is formatted as **Date**, and `Previous_Incidents` is a **Whole Number**.

---

### 2. Five Essential DAX Measures to Create
Click **New Measure** in the Modeling ribbon:

```dax
-- Measure 1: Total Incidents
Total Incidents = COUNTROWS('crime_data_clean')

-- Measure 2: High Severity Count
High Severity Incidents = CALCULATE(COUNTROWS('crime_data_clean'), 'crime_data_clean'[Severity_Level] = "High")

-- Measure 3: High Severity Percentage
High Severity % = DIVIDE([High Severity Incidents], [Total Incidents], 0)

-- Measure 4: Average Previous Incidents
Avg Previous Incidents = AVERAGE('crime_data_clean'[Previous_Incidents])

-- Measure 5: Property Crime Count
Property Crimes = CALCULATE(COUNTROWS('crime_data_clean'), 'crime_data_clean'[Crime_Category] = "Property Crime")
```

---

### 3. Dashboard Canvas Layout

#### Top Section: 5 KPI Cards
- **Card 1**: `[Total Incidents]` &rarr; Display: **1,000**
- **Card 2**: `[High Severity Incidents]` &rarr; Display: **89**
- **Card 3**: `[High Severity %]` &rarr; Format as Percentage &rarr; **8.9%**
- **Card 4**: `[Avg Previous Incidents]` &rarr; Format 1 decimal &rarr; **4.4**
- **Card 5**: Top Crime Mode &rarr; **Theft (32.0%)**

#### Left Sidebar: Interactive Slicers
Add 4 Slicers for quick filtering:
- **Area** (Dropdown)
- **Crime Type** (List)
- **Severity Level** (Horizontal buttons: Low, Medium, High)
- **Month** (Dropdown)

#### Main Canvas: 5 Core Visualizations
1. **Crime Volume by Type**: Clustered Bar Chart (`Crime_Type` on Y-axis, `Total Incidents` on X-axis).
2. **Monthly Crime Trend**: Line Chart (`Month` on X-axis, `Total Incidents` on Y-axis).
3. **Incidents by Area**: Clustered Column Chart (`Area` on X-axis, `Total Incidents` on Y-axis).
4. **Day of Week Distribution**: Column Chart (`Day_of_Week` on X-axis, `Total Incidents` on Y-axis).
5. **Severity Ratio**: Donut Chart (`Severity_Level` as Legend, `Total Incidents` as Values).

---

### 🎓 Power BI Viva Tip
> **Professor:** *"What is the benefit of a Power BI dashboard alongside a Flask website?"*  
> **Answer:** *"Sir/Ma'am, while the Flask website provides operational end-user functionality and real-time model inference (`/predict`), Power BI empowers senior decision-makers with drill-through exploration, cross-filtering, and self-service business intelligence across large datasets."*
