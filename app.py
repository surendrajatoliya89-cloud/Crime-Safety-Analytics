import os
import math
import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify

from database.db_helper import fetch_crime_records

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "crime_data_clean.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "crime_risk_model.pkl")

# 1. Load Dataset for In-Memory KPI & Analytics
if os.path.exists(DATA_PATH):
    df_clean = pd.read_csv(DATA_PATH)
else:
    df_clean = pd.DataFrame()

# 2. Load Trained ML Model Pipeline
model_pipeline = None
if os.path.exists(MODEL_PATH):
    try:
        model_pipeline = joblib.load(MODEL_PATH)
        print("Scikit-learn Random Forest model pipeline loaded successfully with Multi-Year support.")
    except Exception as e:
        print(f"Warning: Failed to load ML model: {e}")

# Precompute unique dropdown options and geographic hierarchies
YEARS = sorted([int(y) for y in df_clean["Year"].unique()], reverse=True) if not df_clean.empty else [2024, 2023, 2022, 2021]
STATES = sorted(df_clean["State"].unique().tolist()) if not df_clean.empty else []
CITIES = sorted(df_clean["City"].unique().tolist()) if not df_clean.empty else []
AREAS = sorted(df_clean["Area"].unique().tolist()) if not df_clean.empty else []
CRIME_TYPES = sorted(df_clean["Crime_Type"].unique().tolist()) if not df_clean.empty else []
LOC_TYPES = sorted(df_clean["Location_Type"].unique().tolist()) if not df_clean.empty else []
TIME_CATS = ["Morning", "Afternoon", "Evening", "Night"]
MONTHS = ["January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WEATHERS = ["Clear", "Cloudy", "Foggy", "Rainy"]

# City Geographic Coordinates for 2D Leaflet Map
CITY_COORDINATES = {
    "Delhi": {"lat": 28.6139, "lng": 77.2090, "state": "Delhi (NCT)"},
    "Mumbai": {"lat": 19.0760, "lng": 72.8777, "state": "Maharashtra"},
    "Pune": {"lat": 18.5204, "lng": 73.8567, "state": "Maharashtra"},
    "Bengaluru": {"lat": 12.9716, "lng": 77.5946, "state": "Karnataka"},
    "Hyderabad": {"lat": 17.3850, "lng": 78.4867, "state": "Telangana"},
    "Chennai": {"lat": 13.0827, "lng": 80.2707, "state": "Tamil Nadu"},
    "Kolkata": {"lat": 22.5726, "lng": 88.3639, "state": "West Bengal"},
    "Ahmedabad": {"lat": 23.0225, "lng": 72.5714, "state": "Gujarat"}
}

# Geographic Hierarchy Mapping (State -> Cities -> Areas)
GEO_HIERARCHY = {}
if not df_clean.empty:
    for s in STATES:
        GEO_HIERARCHY[s] = {}
        s_df = df_clean[df_clean["State"] == s]
        for c in sorted(s_df["City"].unique().tolist()):
            GEO_HIERARCHY[s][c] = sorted(s_df[s_df["City"] == c]["Area"].unique().tolist())


def get_dashboard_kpis():
    """Computes all KPI cards directly from the multi-year dataset."""
    if df_clean.empty:
        return {
            "total_incidents": 0, "total_years_span": "2021-2024", "total_states": 0, "total_cities": 0,
            "most_common_crime": "N/A", "most_common_crime_pct": 0,
            "top_area": "N/A", "top_area_count": 0, "top_severity": "N/A",
            "top_severity_pct": 0, "top_month": "N/A", "top_month_count": 0
        }
    
    total = len(df_clean)
    num_states = df_clean["State"].nunique()
    num_cities = df_clean["City"].nunique()
    min_year = int(df_clean["Year"].min())
    max_year = int(df_clean["Year"].max())
    
    crime_mode = df_clean["Crime_Type"].mode()[0]
    crime_pct = round((df_clean["Crime_Type"] == crime_mode).mean() * 100, 1)
    
    area_mode = df_clean["Area"].mode()[0]
    area_count = int((df_clean["Area"] == area_mode).sum())
    
    sev_mode = df_clean["Severity_Level"].mode()[0]
    sev_pct = round((df_clean["Severity_Level"] == sev_mode).mean() * 100, 1)
    
    month_mode = df_clean["Month"].mode()[0]
    month_count = int((df_clean["Month"] == month_mode).sum())
    
    return {
        "total_incidents": f"{total:,}",
        "total_years_span": f"{min_year}-{max_year}",
        "total_states": num_states,
        "total_cities": num_cities,
        "most_common_crime": crime_mode,
        "most_common_crime_pct": crime_pct,
        "top_area": area_mode,
        "top_area_count": area_count,
        "top_severity": sev_mode,
        "top_severity_pct": sev_pct,
        "top_month": month_mode,
        "top_month_count": month_count
    }


# ====================================================================
# APPLICATION ROUTES
# ====================================================================

@app.route("/")
def dashboard():
    """Route 1: Main Analytics Dashboard with Multi-Year KPIs and Chart.js containers"""
    kpis = get_dashboard_kpis()
    return render_template("index.html", kpis=kpis)


@app.route("/map")
def crime_map():
    """Route 2: Interactive 2D India Crime Map using Leaflet.js with Year Details"""
    city_stats = []
    state_counts = df_clean["State"].value_counts().to_dict() if not df_clean.empty else {}
    year_counts = df_clean["Year"].value_counts().sort_index().to_dict() if not df_clean.empty else {}
    
    if not df_clean.empty:
        for city_name, coords in CITY_COORDINATES.items():
            city_df = df_clean[df_clean["City"] == city_name]
            if not city_df.empty:
                total_cases = len(city_df)
                top_crime = city_df["Crime_Type"].mode()[0]
                high_risk = int((city_df["Crime_Risk_Level"] == "High").sum())
                low_sev = round((city_df["Severity_Level"] == "Low").mean() * 100, 1)
                cases_2024 = int((city_df["Year"] == 2024).sum())
                
                city_stats.append({
                    "city": city_name,
                    "state": coords["state"],
                    "lat": coords["lat"],
                    "lng": coords["lng"],
                    "total": total_cases,
                    "cases_2024": cases_2024,
                    "top_crime": top_crime,
                    "high_risk_count": high_risk,
                    "low_sev_pct": low_sev
                })
        
        city_stats.sort(key=lambda x: x["total"], reverse=True)
        
    return render_template("map.html", city_stats=city_stats, state_counts=state_counts, year_counts=year_counts)


@app.route("/crimes")
def crimes():
    """Route 3: Historical Crime Data Explorer with Year/State/City/Area/Crime Filters"""
    page = request.args.get("page", 1, type=int)
    per_page = 15
    offset = (page - 1) * per_page
    
    search_q = request.args.get("q", "").strip()
    selected_year = request.args.get("year", "All")
    selected_state = request.args.get("state", "All")
    selected_city = request.args.get("city", "All")
    selected_area = request.args.get("area", "All")
    selected_crime = request.args.get("crime", "All")
    
    records, total_count, engine_name = fetch_crime_records(
        limit=per_page, 
        offset=offset, 
        search_query=search_q if search_q else None,
        year_filter=selected_year,
        state_filter=selected_state,
        city_filter=selected_city,
        area_filter=selected_area,
        crime_filter=selected_crime
    )
    
    total_pages = math.ceil(total_count / per_page) if total_count > 0 else 1
    
    return render_template(
        "crimes.html",
        records=records,
        total_count=total_count,
        current_page=page,
        total_pages=total_pages,
        years=YEARS,
        states=STATES,
        cities=CITIES,
        areas=AREAS,
        crime_types=CRIME_TYPES,
        search_query=search_q,
        selected_year=selected_year,
        selected_state=selected_state,
        selected_city=selected_city,
        selected_area=selected_area,
        selected_crime=selected_crime,
        db_source=engine_name
    )


@app.route("/predict", methods=["GET", "POST"])
def prediction():
    """Route 4: Interactive Machine Learning Risk Classification with Year, State, City & Area"""
    prediction_result = None
    explanation = None
    probabilities = None
    form_data = {
        "Year": 2024,
        "State": "Maharashtra",
        "City": "Mumbai",
        "Area": "Colaba",
        "Crime_Type": "Theft",
        "Location_Type": "Street",
        "Time_Category": "Night",
        "Month": "October",
        "Day_of_Week": "Friday",
        "Weather": "Clear",
        "Holiday": "No",
        "Previous_Incidents": 4
    }
    
    options = {
        "years": YEARS,
        "states": STATES,
        "cities": CITIES,
        "areas": AREAS,
        "geo_hierarchy": GEO_HIERARCHY,
        "crime_types": CRIME_TYPES,
        "location_types": LOC_TYPES,
        "time_categories": TIME_CATS,
        "months": MONTHS,
        "days": DAYS,
        "weather": WEATHERS
    }
    
    if request.method == "POST":
        try:
            form_data = {
                "Year": int(request.form.get("Year", 2024)),
                "State": request.form.get("State", "Maharashtra"),
                "City": request.form.get("City", "Mumbai"),
                "Area": request.form.get("Area", "Colaba"),
                "Crime_Type": request.form.get("Crime_Type", "Theft"),
                "Month": request.form.get("Month", "October"),
                "Day_of_Week": request.form.get("Day_of_Week", "Friday"),
                "Time_Category": request.form.get("Time_Category", "Night"),
                "Weather": request.form.get("Weather", "Clear"),
                "Holiday": request.form.get("Holiday", "No"),
                "Location_Type": request.form.get("Location_Type", "Street"),
                "Previous_Incidents": int(request.form.get("Previous_Incidents", 3))
            }
            
            if model_pipeline is not None:
                input_df = pd.DataFrame([form_data])
                
                pred = model_pipeline.predict(input_df)[0]
                prediction_result = pred
                
                if hasattr(model_pipeline, "predict_proba"):
                    probs = model_pipeline.predict_proba(input_df)[0]
                    classes = model_pipeline.classes_
                    probabilities = {cls: round(float(prob) * 100, 1) for cls, prob in zip(classes, probs)}
                
                explanation = (
                    f"Based on historical data for {form_data['Year']} in {form_data['Area']}, {form_data['City']} ({form_data['State']}) "
                    f"during {form_data['Time_Category']} hours with {form_data['Previous_Incidents']} recorded previous incidents, "
                    f"the scenario is classified as {prediction_result} Risk."
                )
        except Exception as e:
            explanation = f"Error generating prediction: {str(e)}"
            
    return render_template(
        "prediction.html",
        options=options,
        form_data=form_data,
        prediction_result=prediction_result,
        explanation=explanation,
        probabilities=probabilities
    )


@app.route("/analytics")
def analytics():
    """Route 5: Multi-Year Visual Analytics & Safety Insights"""
    yearly_stats = []
    if not df_clean.empty:
        for y in sorted(df_clean["Year"].unique(), reverse=True):
            y_df = df_clean[df_clean["Year"] == y]
            yearly_stats.append({
                "year": int(y),
                "total": len(y_df),
                "top_crime": y_df["Crime_Type"].mode()[0],
                "top_state": y_df["State"].mode()[0],
                "top_city": y_df["City"].mode()[0],
                "high_risk_pct": round((y_df["Crime_Risk_Level"] == "High").mean() * 100, 1)
            })
    return render_template("analytics.html", yearly_stats=yearly_stats)


@app.route("/about")
def about():
    """Route 6: Project Methodology, Ethical Considerations and Viva Guide"""
    return render_template("about.html")


@app.route("/api/charts-data")
def charts_data():
    """JSON API for Chart.js rendering across Year, State, City, Crime Types, and Severities"""
    if df_clean.empty:
        return jsonify({})
        
    year_counts = {str(k): int(v) for k, v in df_clean["Year"].value_counts().sort_index().items()}
    state_counts = df_clean["State"].value_counts().to_dict()
    city_counts = df_clean["City"].value_counts().to_dict()
    crime_types = df_clean["Crime_Type"].value_counts().to_dict()
    
    month_order = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    monthly_trends = df_clean["Month"].value_counts().reindex(month_order).fillna(0).astype(int).to_dict()
    
    area_counts = df_clean["Area"].value_counts().head(8).to_dict()
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_counts = df_clean["Day_of_Week"].value_counts().reindex(day_order).fillna(0).astype(int).to_dict()
    severity_counts = df_clean["Severity_Level"].value_counts().to_dict()
    
    return jsonify({
        "year_counts": year_counts,
        "state_counts": state_counts,
        "city_counts": city_counts,
        "crime_types": crime_types,
        "monthly_trends": monthly_trends,
        "area_counts": area_counts,
        "day_counts": day_counts,
        "severity_counts": severity_counts
    })


if __name__ == "__main__":
    print("=" * 60)
    print("CrimeWatch Analytics - Running with Multi-Year (2021-2024) Support!")
    print("Open your browser: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False)
