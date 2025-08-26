import streamlit as st
import pandas as pd
import numpy as np
from utils.preprocessing import map_company_size, map_education_level, map_exp_level, process_required_skills, transform_skills
from utils.model_utils import load_model, predict_salary, predict_class
import os
from dotenv import load_dotenv

load_dotenv()

REG_MODEL_PATH = os.getenv("REG_MODEL_PATH")
CLASS_MODEL_PATH = os.getenv("CLASS_MODEL_PATH")

st.header("Batch Job Analysis")
st.write("Upload a CSV file with job details to get salary predictions.")

csv_file = st.file_uploader("Upload CSV", type=["csv"])

if csv_file:
    data = pd.read_csv(csv_file)
    df = data.copy()

    # Preprocess the DataFrame
    df = map_company_size(df)
    df = map_education_level(df)
    df = map_exp_level(df)
    df = process_required_skills(df)
    df = transform_skills(df)

    class_model = load_model(CLASS_MODEL_PATH)
    reg_model = load_model(REG_MODEL_PATH)

    salary_predictions = []
    class_predictions = []

    for _, row in df.iterrows():
        row_df = pd.DataFrame([row])   # single row as DataFrame
        salary = predict_salary(reg_model, row_df)
        job_class = predict_class(class_model, row_df)
        salary_predictions.append(np.round(salary, 2))
        class_predictions.append("High Paying" if job_class == 1 else "Low Paying")

    data["predicted_salary"] = salary_predictions
    data["predicted_class"] = class_predictions

    st.write("Data Preview:")
    st.dataframe(data)