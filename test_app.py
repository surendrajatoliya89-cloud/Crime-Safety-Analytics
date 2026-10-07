from app import app

client = app.test_client()

routes = [
    "/", "/map", "/crimes", "/predict", "/analytics", "/about", 
    "/api/charts-data", "/crimes?year=2023&state=Maharashtra&city=Mumbai"
]

print("TESTING FLASK ROUTES WITH MULTI-YEAR SUPPORT:")
all_passed = True
for r in routes:
    res = client.get(r)
    status = res.status_code
    print(f"  Route '{r}': Status {status}")
    if status != 200:
        all_passed = False

post_res = client.post("/predict", data={
    "Year": "2024",
    "State": "Maharashtra",
    "City": "Mumbai",
    "Area": "Colaba",
    "Crime_Type": "Vehicle Theft",
    "Month": "March",
    "Day_of_Week": "Friday",
    "Time_Category": "Night",
    "Weather": "Clear",
    "Holiday": "No",
    "Location_Type": "Parking Complex",
    "Previous_Incidents": "8"
})
print(f"  POST '/predict' (with Year): Status {post_res.status_code}")
if post_res.status_code != 200 or (b"HIGH RISK" not in post_res.data and b"MEDIUM RISK" not in post_res.data and b"LOW RISK" not in post_res.data):
    all_passed = False

print("\nALL FLASK ROUTES WITH MULTI-YEAR VERIFIED SUCCESSFULLY!" if all_passed else "\nSOME ROUTES FAILED!")
