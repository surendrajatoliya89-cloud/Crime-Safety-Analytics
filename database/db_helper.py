import os
import sqlite3
import pandas as pd

try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "crime_analytics"
}

def get_db_connection():
    if MYSQL_AVAILABLE:
        try:
            conn = mysql.connector.connect(**MYSQL_CONFIG)
            if conn.is_connected():
                return conn, "MySQL"
        except Exception:
            pass

    sqlite_path = os.path.join(os.path.dirname(__file__), "crime_analytics.db")
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    return conn, "SQLite (Local Fail-safe)"

def fetch_crime_records(limit=15, offset=0, search_query=None, year_filter=None, state_filter=None, city_filter=None, area_filter=None, crime_filter=None):
    conn, engine = get_db_connection()
    cursor = conn.cursor()
    
    base_query = "FROM crime_records WHERE 1=1"
    params = []
    
    if search_query:
        base_query += " AND (Incident_ID LIKE ? OR State LIKE ? OR City LIKE ? OR Area LIKE ? OR Crime_Type LIKE ?)"
        term = f"%{search_query}%"
        params.extend([term, term, term, term, term])

    if year_filter and str(year_filter) != "All":
        base_query += " AND Year = ?"
        params.append(int(year_filter))
        
    if state_filter and state_filter != "All":
        base_query += " AND State = ?"
        params.append(state_filter)

    if city_filter and city_filter != "All":
        base_query += " AND City = ?"
        params.append(city_filter)

    if area_filter and area_filter != "All":
        base_query += " AND Area = ?"
        params.append(area_filter)
        
    if crime_filter and crime_filter != "All":
        base_query += " AND Crime_Type = ?"
        params.append(crime_filter)
        
    count_sql = f"SELECT COUNT(*) {base_query}"
    if engine == "MySQL":
        count_sql = count_sql.replace("?", "%s")
    cursor.execute(count_sql, params)
    total_count = cursor.fetchone()[0]
    
    data_sql = f"SELECT * {base_query} ORDER BY Date DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    if engine == "MySQL":
        data_sql = data_sql.replace("?", "%s")
        
    cursor.execute(data_sql, params)
    rows = cursor.fetchall()
    
    if engine == "MySQL":
        columns = [col[0] for col in cursor.description]
        records = [dict(zip(columns, row)) for row in rows]
    else:
        records = [dict(row) for row in rows]
        
    conn.close()
    return records, total_count, engine
