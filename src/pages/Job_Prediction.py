from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
from pathlib import Path
import numpy as np
from utils.preprocessing import map_company_size, map_education_level, map_exp_level, process_required_skills, transform_skills
from utils.model_utils import load_model, predict_salary, predict_class

load_dotenv()

st.title("💼 Job Details")

st.header("Enter the job information to get a salary prediction")

REG_MODEL_PATH = os.getenv("REG_MODEL_PATH")
CLASS_MODEL_PATH = os.getenv("CLASS_MODEL_PATH")

if not REG_MODEL_PATH or not CLASS_MODEL_PATH:
    st.error("Model paths are not set.")
    st.stop()

reg_model = load_model(REG_MODEL_PATH)
class_model = load_model(CLASS_MODEL_PATH)

region_country = {'Asia': ['China', 'India', 'Singapore', 'South Korea', 'Israel', 'Japan'],
 'Europe': ['Switzerland',
  'France',
  'Germany',
  'United Kingdom',
  'Austria',
  'Sweden',
  'Norway',
  'Netherlands',
  'Ireland',
  'Denmark',
  'Finland'],
 'North America': ['Canada', 'United States'],
 'Oceania': ['Australia'],
 'Africa': ['Coming soon... 😅']
 }

job_field = st.selectbox(
    "Select Job Field",
    ['Scientist', 'Engineer', 'Specialist', 'Consultant', 'Architect',
       'Analyst', 'Manager', 'AI', 'Researcher']
)

skills = st.text_input("Key skills (comma -separated)", placeholder="E.g Python, SQL, NLP")
skills = [skill.strip() for skill in skills.split(",")]


exp_level = st.selectbox(
    "Experience level (Entry, Middle, Senior, Expert)",
    ["EN", "MI", "SE", "EX"]
)

employment_type = st.selectbox(
    "Employment Type (Full-time, Part-time, Contract, Freelance)",
    ["FT", "PT", "CT", "FL"]
)

exp_years_col, edu_level_col = st.columns(2)

with exp_years_col:
    exp_years = st.number_input("Years of Experience", min_value=0, value=0)

with edu_level_col:
    edu_level = st.selectbox(
        "Education Level (Associate's, Bachelor's, Master's, PhD)",
        ["Associate", "Bachelor's", "Master's", "PhD"]
    )

region_col, location_col = st.columns(2)

with region_col:
    selected_region = st.selectbox(
        "Region",
        list(region_country.keys())
    )

with location_col:
    selected_location = st.selectbox(
        "Location",
        region_country[selected_region]
    )

company_size_col, remote_ratio_col = st.columns(2)

with company_size_col:
    company_size = st.selectbox(
        "Company Size (Small, Medium, Large)",
        ["S", "M", "L"]
    )

with remote_ratio_col:
    remote_ratio = st.select_slider(
        "Remote Work Ratio (0 - 100%)",
        options=[0, 50, 100]
)

industry = st.selectbox(
    "Industry",
    ['Automotive', 'Media', 'Education', 'Consulting', 'Healthcare',
       'Gaming', 'Government', 'Telecommunications', 'Manufacturing',
       'Energy', 'Technology', 'Real Estate', 'Finance', 'Transportation',
       'Retail']
)

benefit_score = st.slider(
    "Benefit Score (5.0 - 10.0)",
    min_value=5.0,
    max_value=10.0,
    value=5.0,
    step=0.1
)

job_desc_col, days_until_deadline_col = st.columns(2)

with job_desc_col:
    job_desc_length = st.number_input("Job Description Length (in characters)", min_value=0, value=0)

with days_until_deadline_col:
    days_until_deadline = st.number_input("Days Until Deadline", min_value=0, value=0)


predict_btn = st.button("Predict Salary", type="primary")



if predict_btn:
    df = pd.DataFrame({
        "experience_level": exp_level,
        "employment_type": employment_type,
        "company_location": selected_location,
        "company_size": company_size,
        "education_required": edu_level,
        "years_experience": exp_years,
        "industry": industry,
        "job_description_length": job_desc_length,
        "benefits_score": benefit_score,
        "days_until_deadline": days_until_deadline,
        "remote_ratio": remote_ratio,
        "broader_job_title": job_field,
        "required_skills": [skills],
    })

    df = map_company_size(df)
    df = map_education_level(df)
    df = map_exp_level(df)
    df = process_required_skills(df)
    df = transform_skills(df)

    salary_prediction = predict_salary(reg_model, df)
    class_prediction = predict_class(class_model, df)

    st.success(f"Predicted Salary: ${salary_prediction[0]:,.2f}")
    if class_prediction == 0:
        st.error("Predicted Class: Low Pay")
    else:
        st.success(f"Predicted Class: High Pay")
