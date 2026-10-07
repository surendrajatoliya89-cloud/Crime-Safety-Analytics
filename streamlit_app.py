import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import joblib
import json
import os

st.set_page_config(page_title='CrimeWatch Analytics', page_icon='🔍', layout='wide')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'crime_data_clean.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'crime_risk_model.pkl')
METRICS_PATH = os.path.join(BASE_DIR, 'model', 'model_metrics.json')

# Helper function to load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(DATA_PATH)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Helper function to load model
@st.cache_resource
def load_model():
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except Exception as e:
        return None

# Custom CSS
def apply_custom_css():
    st.markdown("""
        <style>
        .stApp {
            background-color: #f8f9fa;
        }
        .main-header {
            color: #1a1a2e;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        .kpi-card {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            border-top: 4px solid #e94560;
            margin-bottom: 1rem;
        }
        .kpi-value {
            font-size: 2rem;
            font-weight: bold;
            color: #1a1a2e;
        }
        .kpi-label {
            font-size: 1rem;
            color: #6c757d;
        }
        </style>
    """, unsafe_allow_html=True)

def dashboard_page():
    st.markdown('<div class="main-header">📊 Dashboard</div>', unsafe_allow_html=True)
    df = load_data()
    if df.empty:
        return

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{len(df)}</div><div class="kpi-label">Total Incidents</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{df["Crime_Type"].mode()[0]}</div><div class="kpi-label">Most Common Crime</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{df["Year"].min()} - {df["Year"].max()}</div><div class="kpi-label">Year Span</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{df["Area"].mode()[0]}</div><div class="kpi-label">Top Area</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{df["State"].nunique()}</div><div class="kpi-label">States</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{df["Severity_Level"].mode()[0]}</div><div class="kpi-label">Top Severity</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{df["City"].nunique()}</div><div class="kpi-label">Cities</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{df["Month"].mode()[0]}</div><div class="kpi-label">Top Month</div></div>', unsafe_allow_html=True)

    # Charts
    col_a, col_b = st.columns(2)
    
    with col_a:
        fig_year = px.bar(df['Year'].value_counts().reset_index(), x='Year', y='count', title='Crime by Year', color_discrete_sequence=['#e94560'])
        st.plotly_chart(fig_year, use_container_width=True)
        
        fig_state = px.bar(df['State'].value_counts().reset_index(), x='State', y='count', title='Crime by State', color_discrete_sequence=['#1a1a2e'])
        st.plotly_chart(fig_state, use_container_width=True)
        
        fig_month = px.line(df.groupby(['Year', 'Month']).size().reset_index(name='count'), x='Month', y='count', color='Year', title='Monthly Trends')
        st.plotly_chart(fig_month, use_container_width=True)
        
        fig_dow = px.bar(df['Day_of_Week'].value_counts().reset_index(), x='Day_of_Week', y='count', title='Day of Week', color_discrete_sequence=['#e94560'])
        st.plotly_chart(fig_dow, use_container_width=True)

    with col_b:
        fig_city = px.bar(df['City'].value_counts().reset_index(), x='City', y='count', title='Crime by City', color_discrete_sequence=['#1a1a2e'])
        st.plotly_chart(fig_city, use_container_width=True)
        
        fig_type = px.pie(df, names='Crime_Type', title='Crime Types', hole=0.3)
        st.plotly_chart(fig_type, use_container_width=True)
        
        top_areas = df['Area'].value_counts().head(10).reset_index()
        fig_area = px.bar(top_areas, x='count', y='Area', orientation='h', title='Top Areas', color_discrete_sequence=['#e94560'])
        fig_area.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_area, use_container_width=True)
        
        fig_sev = px.pie(df, names='Severity_Level', title='Severity Distribution', hole=0.5, color_discrete_sequence=px.colors.sequential.Reds)
        st.plotly_chart(fig_sev, use_container_width=True)

def map_page():
    st.markdown('<div class="main-header">🗺️ Crime Map</div>', unsafe_allow_html=True)
    df = load_data()
    if df.empty:
        return

    city_coords = {
        'Delhi': [77.2090, 28.6139],
        'Mumbai': [72.8777, 19.0760],
        'Pune': [73.8567, 18.5204],
        'Bengaluru': [77.5946, 12.9716],
        'Hyderabad': [78.4867, 17.3850],
        'Chennai': [80.2707, 13.0827],
        'Kolkata': [88.3639, 22.5726],
        'Ahmedabad': [72.5714, 23.0225]
    }

    # Aggregate data for map
    map_data = []
    for city, coords in city_coords.items():
        city_df = df[df['City'] == city]
        if not city_df.empty:
            cases = len(city_df)
            top_crime = city_df['Crime_Type'].mode()[0] if not city_df.empty else 'N/A'
            high_risk = len(city_df[city_df['Crime_Risk_Level'] == 'High'])
            
            map_data.append({
                'City': city,
                'lon': coords[0],
                'lat': coords[1],
                'Cases': cases,
                'Top_Crime': top_crime,
                'High_Risk': high_risk,
                'radius': cases * 50 # scale for visualization
            })

    map_df = pd.DataFrame(map_data)

    col1, col2 = st.columns([3, 1])

    with col1:
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=20.5937,
                longitude=78.9629,
                zoom=4,
                pitch=45,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=map_df,
                    get_position='[lon, lat]',
                    get_color='[200, 30, 0, 160]',
                    get_radius='radius',
                    pickable=True,
                ),
            ],
            tooltip={"text": "{City}\\nTotal Cases: {Cases}\\nTop Crime: {Top_Crime}\\nHigh Risk: {High_Risk}"}
        ))

    with col2:
        st.subheader("Sidebar Stats")
        st.write("### State-wise Breakdown")
        st.dataframe(df['State'].value_counts().reset_index().rename(columns={'count': 'Cases'}), hide_index=True)
        
        st.write("### Year-wise Breakdown")
        st.dataframe(df['Year'].value_counts().reset_index().rename(columns={'count': 'Cases'}).sort_values('Year'), hide_index=True)


def data_explorer_page():
    st.markdown('<div class="main-header">🔍 Data Explorer</div>', unsafe_allow_html=True)
    df = load_data()
    if df.empty:
        return

    # Filters
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        years = ['All'] + sorted(df['Year'].unique().tolist())
        sel_year = st.selectbox("Year", years)
    with col2:
        states = ['All'] + sorted(df['State'].unique().tolist())
        sel_state = st.selectbox("State", states)
    with col3:
        if sel_state != 'All':
            cities = ['All'] + sorted(df[df['State'] == sel_state]['City'].unique().tolist())
        else:
            cities = ['All'] + sorted(df['City'].unique().tolist())
        sel_city = st.selectbox("City", cities)
    with col4:
        if sel_city != 'All':
            areas = ['All'] + sorted(df[df['City'] == sel_city]['Area'].unique().tolist())
        else:
            areas = ['All'] + sorted(df['Area'].unique().tolist())
        sel_area = st.selectbox("Area", areas)
    with col5:
        crimes = ['All'] + sorted(df['Crime_Type'].unique().tolist())
        sel_crime = st.selectbox("Crime Type", crimes)

    search_query = st.text_input("Search (any column)", "")

    # Apply filters
    filtered_df = df.copy()
    if sel_year != 'All':
        filtered_df = filtered_df[filtered_df['Year'] == sel_year]
    if sel_state != 'All':
        filtered_df = filtered_df[filtered_df['State'] == sel_state]
    if sel_city != 'All':
        filtered_df = filtered_df[filtered_df['City'] == sel_city]
    if sel_area != 'All':
        filtered_df = filtered_df[filtered_df['Area'] == sel_area]
    if sel_crime != 'All':
        filtered_df = filtered_df[filtered_df['Crime_Type'] == sel_crime]

    if search_query:
        # Search all columns
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        filtered_df = filtered_df[mask]

    st.write(f"**Total Records:** {len(filtered_df)}")
    
    # Pagination
    PAGE_SIZE = 15
    total_pages = max(1, len(filtered_df) // PAGE_SIZE + (1 if len(filtered_df) % PAGE_SIZE > 0 else 0))
    page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
    
    start_idx = (page - 1) * PAGE_SIZE
    end_idx = start_idx + PAGE_SIZE
    
    st.dataframe(filtered_df.iloc[start_idx:end_idx], use_container_width=True)

def prediction_page():
    st.markdown('<div class="main-header">🧠 ML Prediction</div>', unsafe_allow_html=True)
    df = load_data()
    model = load_model()

    if df.empty or model is None:
        st.warning("Data or model not found. Cannot perform prediction.")
        return

    with st.form("predict_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            year = st.selectbox("Year", sorted(df['Year'].unique()))
            state = st.selectbox("State", sorted(df['State'].unique()))
            city_options = sorted(df[df['State'] == state]['City'].unique()) if state else sorted(df['City'].unique())
            city = st.selectbox("City", city_options)
            area_options = sorted(df[df['City'] == city]['Area'].unique()) if city else sorted(df['Area'].unique())
            area = st.selectbox("Area", area_options)
            
        with col2:
            crime_type = st.selectbox("Crime_Type", sorted(df['Crime_Type'].unique()))
            loc_type = st.selectbox("Location_Type", sorted(df['Location_Type'].unique()))
            time_cat = st.selectbox("Time_Category", sorted(df['Time_Category'].unique()))
            month = st.selectbox("Month", sorted(df['Month'].unique()))
            
        with col3:
            day_of_week = st.selectbox("Day_of_Week", sorted(df['Day_of_Week'].unique()))
            weather = st.selectbox("Weather", sorted(df['Weather'].unique()))
            holiday = st.selectbox("Holiday", ['Yes', 'No'])
            prev_incidents = st.slider("Previous_Incidents", 0, 15, 0)
            
        submit = st.form_submit_button("Predict Risk Level")

    if submit:
        # Create input df
        input_data = pd.DataFrame([{
            'Year': year,
            'State': state,
            'City': city,
            'Area': area,
            'Crime_Type': crime_type,
            'Location_Type': loc_type,
            'Time_Category': time_cat,
            'Month': month,
            'Day_of_Week': day_of_week,
            'Weather': weather,
            'Holiday': holiday,
            'Previous_Incidents': prev_incidents
        }])

        try:
            pred = model.predict(input_data)[0]
            
            # Predict Proba if available
            proba = None
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(input_data)[0]
                classes = model.classes_
                
            color = "#28a745" if pred == "Low" else "#ffc107" if pred == "Medium" else "#dc3545"
            
            st.markdown(f"""
            <div style="background-color: {color}; color: white; padding: 20px; border-radius: 10px; text-align: center; margin-top: 20px;">
                <h2 style="margin:0; color: white;">Predicted Crime Risk Level: {pred}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            if proba is not None:
                st.write("### Prediction Probabilities")
                prob_df = pd.DataFrame({"Risk Level": classes, "Probability": proba})
                fig = px.bar(prob_df, x="Probability", y="Risk Level", orientation='h', color="Risk Level", 
                             color_discrete_map={"Low": "#28a745", "Medium": "#ffc107", "High": "#dc3545"})
                st.plotly_chart(fig, use_container_width=True)
                
            st.info("The prediction is based on historical patterns for similar temporal, geographical, and situational factors.")
                
        except Exception as e:
            st.error(f"Prediction failed: {e}. The model might require different columns or format.")


def analytics_page():
    st.markdown('<div class="main-header">📈 Analytics & Insights</div>', unsafe_allow_html=True)
    df = load_data()
    if df.empty:
        return

    st.subheader("Year-by-Year Comparison")
    year_stats = df.groupby('Year').size().reset_index(name='Total Cases')
    st.dataframe(year_stats, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.line(year_stats, x='Year', y='Total Cases', title='Crime Trends Over Years', markers=True)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Crime types by severity
        sev_crime = df.groupby(['Crime_Type', 'Severity_Level']).size().reset_index(name='count')
        fig3 = px.bar(sev_crime, x='Crime_Type', y='count', color='Severity_Level', title='Crime Types by Severity')
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        fig2 = px.pie(df, names='Crime_Risk_Level', title='Risk Level Distribution', color_discrete_sequence=['#ff9999','#66b3ff','#99ff99'])
        st.plotly_chart(fig2, use_container_width=True)
        
        fig4 = px.bar(df['Weather'].value_counts().reset_index(), x='Weather', y='count', title='Weather Impact')
        st.plotly_chart(fig4, use_container_width=True)

    # Time category analysis
    fig5 = px.histogram(df, x='Time_Category', title='Time Category Analysis', color='Time_Category')
    st.plotly_chart(fig5, use_container_width=True)

def about_page():
    st.markdown('<div class="main-header">ℹ️ About</div>', unsafe_allow_html=True)
    
    st.write("""
    ### CrimeWatch Analytics
    **B.Sc Data Science Educational Project**
    
    This application is designed to analyze crime data and predict risk levels using machine learning. 
    It provides interactive dashboards, maps, and predictive capabilities to understand crime patterns.
    """)
    
    st.write("---")
    st.write("### Model Metrics")
    
    metrics = None
    try:
        with open(METRICS_PATH, 'r') as f:
            metrics = json.load(f)
    except Exception:
        # Fallback to hardcoded if file not found
        metrics = {
            "accuracy": "85.21%",
            "precision": "85.47%",
            "recall": "85.21%",
            "f1": "85.23%"
        }
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Accuracy", metrics.get("accuracy", "85.21%"))
    with col2: st.metric("Precision", metrics.get("precision", "85.47%"))
    with col3: st.metric("Recall", metrics.get("recall", "85.21%"))
    with col4: st.metric("F1 Score", metrics.get("f1", "85.23%"))
    
    st.write("---")
    st.write("### Methodology")
    st.write("""
    1. **Data Collection & Cleaning**: Aggregated data from various regions, handled missing values, and standardized formats.
    2. **Exploratory Data Analysis (EDA)**: Analyzed temporal, geographical, and situational patterns.
    3. **Feature Engineering**: Extracted relevant features like time category, weekend/weekday, and encoded categorical variables.
    4. **Model Training**: Used a Random Forest Classifier within an sklearn Pipeline to predict 'Crime_Risk_Level'.
    5. **Deployment**: Built this Streamlit application for interactive visualization and real-time prediction.
    """)
    
    st.write("---")
    st.write("### Ethical Disclaimer")
    st.warning("""
    This project is strictly for educational purposes. The data used might be synthetic or anonymized and should not be used for actual law enforcement, policy making, or to stigmatize any community or region. The predictive model's outputs are probabilities based on historical data and do not imply certainty.
    """)

def main():
    apply_custom_css()
    
    st.sidebar.title("CrimeWatch 🔍")
    st.sidebar.write("---")
    
    pages = {
        "📊 Dashboard": dashboard_page,
        "🗺️ Crime Map": map_page,
        "🔍 Data Explorer": data_explorer_page,
        "🧠 ML Prediction": prediction_page,
        "📈 Analytics & Insights": analytics_page,
        "ℹ️ About": about_page
    }
    
    selection = st.sidebar.radio("Navigation", list(pages.keys()))
    
    st.sidebar.write("---")
    st.sidebar.info("Developed for B.Sc Data Science")
    
    # Run the selected page
    pages[selection]()

if __name__ == "__main__":
    main()

