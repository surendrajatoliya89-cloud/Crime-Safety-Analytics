-- ====================================================================
-- CrimeWatch Analytics - MySQL Database Schema & Analytical Queries
-- Database Name: crime_analytics
-- Target Table:  crime_records
-- ====================================================================

-- 1. Create Database
CREATE DATABASE IF NOT EXISTS crime_analytics;
USE crime_analytics;

-- 2. Create Table
CREATE TABLE IF NOT EXISTS crime_records (
    Incident_ID VARCHAR(20) PRIMARY KEY,
    Date DATE NOT NULL,
    Year INT NOT NULL,
    Month VARCHAR(20) NOT NULL,
    Day_of_Week VARCHAR(20) NOT NULL,
    Time_Category VARCHAR(20) NOT NULL,
    City VARCHAR(50) NOT NULL,
    Area VARCHAR(50) NOT NULL,
    Location_Type VARCHAR(50) NOT NULL,
    Crime_Type VARCHAR(50) NOT NULL,
    Crime_Category VARCHAR(50) NOT NULL,
    Severity_Level VARCHAR(20) NOT NULL,
    Victim_Age INT,
    Victim_Gender VARCHAR(20),
    Weather VARCHAR(20),
    Holiday VARCHAR(10),
    Previous_Incidents INT DEFAULT 0,
    Crime_Risk_Level VARCHAR(20) NOT NULL
);

-- ====================================================================
-- TOP 10 VIVA-READY ANALYTICAL SQL QUERIES
-- ====================================================================

-- Query 1: Total reported incidents
SELECT COUNT(*) AS total_incidents FROM crime_records;

-- Query 2: Crime count and percentage by Crime Type
SELECT 
    Crime_Type, 
    COUNT(*) AS incident_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM crime_records), 2) AS percentage
FROM crime_records
GROUP BY Crime_Type
ORDER BY incident_count DESC;

-- Query 3: Incidents count across geographical Areas
SELECT 
    Area, 
    COUNT(*) AS reported_crimes
FROM crime_records
GROUP BY Area
ORDER BY reported_crimes DESC;

-- Query 4: Monthly incident progression
SELECT 
    Month, 
    COUNT(*) AS monthly_total
FROM crime_records
GROUP BY Month
ORDER BY monthly_total DESC;

-- Query 5: Incident breakdown by Day of the Week
SELECT 
    Day_of_Week, 
    COUNT(*) AS total_crimes
FROM crime_records
GROUP BY Day_of_Week
ORDER BY total_crimes DESC;

-- Query 6: Severity Level distribution
SELECT 
    Severity_Level, 
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM crime_records), 2) AS percentage
FROM crime_records
GROUP BY Severity_Level
ORDER BY count DESC;

-- Query 7: Most common Crime Type in each Area (Subquery/Window)
SELECT Area, Crime_Type, COUNT(*) as incidents
FROM crime_records
GROUP BY Area, Crime_Type
HAVING incidents = (
    SELECT MAX(sub_count) FROM (
        SELECT Area as sub_area, Crime_Type as sub_type, COUNT(*) as sub_count 
        FROM crime_records 
        GROUP BY sub_area, sub_type
    ) t WHERE t.sub_area = crime_records.Area
);

-- Query 8: Average previous incidents per Area
SELECT 
    Area, 
    ROUND(AVG(Previous_Incidents), 2) AS avg_historical_incidents
FROM crime_records
GROUP BY Area
ORDER BY avg_historical_incidents DESC;

-- Query 9: High-Risk incidents by Time Category
SELECT 
    Time_Category, 
    COUNT(*) AS high_risk_count
FROM crime_records
WHERE Crime_Risk_Level = 'High'
GROUP BY Time_Category
ORDER BY high_risk_count DESC;

-- Query 10: Holiday vs. Non-Holiday Incident frequency
SELECT 
    Holiday, 
    COUNT(*) AS total_incidents,
    ROUND(AVG(Previous_Incidents), 2) AS avg_prev_incidents
FROM crime_records
GROUP BY Holiday;
