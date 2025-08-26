import pandas as pd
import joblib
import os
from dotenv import load_dotenv

load_dotenv()

MBL_PATH = os.getenv("MLB_PATH", "models/mlb.pkl")

exp_level = {
    'EN': 0,
    'MI': 1,
    'SE': 2,
    'EX': 3
}

company_size = {
    'S': 0,
    'M': 1,
    'L': 2
}

education_map = {
    "Associate": 0,
    "Bachelor": 1,
    "Master": 2,
    "PhD": 3
}

def map_exp_level(df):
    df['experience_level'] = df['experience_level'].map(exp_level)
    return df

def map_company_size(df):
    df['company_size'] = df['company_size'].map(company_size)
    return df

def map_education_level(df):
    df['education_required'] = df['education_required'].map(education_map)
    return df

def process_required_skills(df):
    df["required_skills"] = df["required_skills"].apply(lambda x: [skill.strip().lower().replace(" ", "_") for skill in x])
    return df


def transform_skills(df, skills_col="required_skills", prefix="skill_", load_path=MBL_PATH):
    """
    Loads a fitted MultiLabelBinarizer and transforms new data consistently.
    
    Args:
        df (pd.DataFrame): Input dataframe with a column of lists.
        skills_col (str): Column containing list of skills.
        prefix (str): Prefix for encoded skill columns.
        load_path (str): Path to fitted MultiLabelBinarizer.
    
    Returns:
        pd.DataFrame: Original df + encoded skill columns
    """
    # Load previously fitted encoder
    mlb = joblib.load(load_path)
    
    skills_encoded = mlb.transform(df[skills_col])
    skills_df = pd.DataFrame(
        skills_encoded, 
        columns=[f"{prefix}{s.lower().replace(' ', '_')}" for s in mlb.classes_]
    )
    
    df = df.reset_index(drop=True)
    return pd.concat([df.drop(columns=[skills_col]), skills_df], axis=1)