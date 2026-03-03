from backend.hospital_service import get_recommendations

# Simulated user location (Banjara Hills area)
USER_LAT = 17.4123
USER_LON = 78.4481

# Test categories one by one
test_categories = [
    "ENT",
    "Dermatology",
    "Orthopedics",
    "Gastroenterology"
]

for category in test_categories:
    print("\n==============================")
    print("CATEGORY:", category)
    print("==============================")

    results = get_recommendations(
        category=category,
        user_lat=USER_LAT,
        user_lon=USER_LON
    )

    if not results:
        print("No hospitals found.")
        continue

    for h in results:
        print("\nHospital:", h["hospital_name"])
        print("Area:", h["area"])
        print("Distance (km):", h["distance_km"])
        print("Doctors:")

        if not h["doctors"]:
            print("  No doctors listed.")
        else:
            for d in h["doctors"]:
                print(
                    f"  {d['doctor_name']} "
                    f"({d['experience_years']} yrs, ₹{d['consultation_fee']})"
                )
