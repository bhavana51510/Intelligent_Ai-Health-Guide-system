from backend.data_loader import (
    load_hospitals,
    load_departments,
    load_hospital_departments,
    load_doctors
)

def get_recommendations(category, user_lat, user_lon):
    hospitals = load_hospitals()
    departments = load_departments()
    hospital_departments = load_hospital_departments()
    doctors = load_doctors()

    # 1. Resolve department_id
    dept_row = departments[
        departments["department_name"].str.lower() == category.lower()
    ]

    if dept_row.empty:
        return []

    dept_id = dept_row.iloc[0]["department_id"]

    # 2. Hospitals offering this department
    eligible_hospital_ids = hospital_departments[
        hospital_departments["department_id"] == dept_id
    ]["hospital_id"].unique()

    eligible_hospitals = hospitals[
        hospitals["hospital_id"].isin(eligible_hospital_ids)
    ]

    results = []

    for _, hosp in eligible_hospitals.iterrows():

        hosp_doctors = doctors[
            (doctors["hospital_id"] == hosp["hospital_id"]) &
            (doctors["department_id"] == dept_id)
        ]

        results.append({
            "hospital_id": hosp["hospital_id"],
            "hospital_name": hosp["hospital_name"],
            "area": hosp["area"],
            "city": hosp["city"],
            "phone": hosp["phone"],
            "address": hosp["address"],
            "place_id": hosp["place_id"],
            "doctors": [
                {
                    "doctor_name": doc["doctor_name"],
                    "experience_years": int(doc["experience_years"]),
                    "consultation_fee": int(doc["consultation_fee"])
                }
                for _, doc in hosp_doctors.iterrows()
            ]
        })

    return results
