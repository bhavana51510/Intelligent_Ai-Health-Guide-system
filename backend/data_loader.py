import pandas as pd

BASE_PATH = "data/hospitals/"

def load_hospitals():
    return pd.read_csv(BASE_PATH + "hospitals.csv")

def load_departments():
    return pd.read_csv(BASE_PATH + "departments.csv")

def load_hospital_departments():
    return pd.read_csv(BASE_PATH + "hospital_departments.csv")

def load_doctors():
    return pd.read_csv(BASE_PATH + "doctors.csv")
