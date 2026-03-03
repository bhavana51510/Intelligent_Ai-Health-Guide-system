from backend.data_loader import (
    load_hospitals,
    load_departments,
    load_hospital_departments,
    load_doctors
)

def run_integrity_checks():
    hospitals = load_hospitals()
    departments = load_departments()
    hospital_departments = load_hospital_departments()
    doctors = load_doctors()

    hospital_ids = set(hospitals["hospital_id"])
    department_ids = set(departments["department_id"])

    assert hospital_departments["hospital_id"].isin(hospital_ids).all(), \
        "Invalid hospital_id in hospital_departments.csv"

    assert hospital_departments["department_id"].isin(department_ids).all(), \
        "Invalid department_id in hospital_departments.csv"

    assert doctors["hospital_id"].isin(hospital_ids).all(), \
        "Invalid hospital_id in doctors.csv"

    assert doctors["department_id"].isin(department_ids).all(), \
        "Invalid department_id in doctors.csv"

    assert hospitals["latitude"].notnull().all(), "Missing latitude"
    assert hospitals["longitude"].notnull().all(), "Missing longitude"

    print("Integrity checks passed successfully.")
