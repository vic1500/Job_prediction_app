import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import uuid
from collections import Counter


def plot_bar_chart(data, x, y, title="Bar Chart", xlabel="X-axis", ylabel="Y-axis"):
    # plt.style.use("dark_background")
    # fig, ax = plt.subplots()
    data_grouped = data.groupby(x)[y].mean().reset_index().sort_values(by=y)
    # ax.barh(data_grouped[x], data_grouped[y], color='skyblue')
    # ax.set_title(title)
    # ax.set_xlabel(xlabel)
    # ax.set_ylabel(ylabel)
    data_grouped = data_grouped.reset_index(drop=True)

    fig = px.bar(
        data_grouped,
        x=y,
        y=x,
        labels={x: ylabel, y: xlabel},
        title=title,
    )
    st.plotly_chart(fig, key=uuid.uuid4())


def salary_by_industry(df):
    industry_salary = df.groupby('industry')['salary_usd'].mean().sort_values()

    industry_salary = industry_salary.reset_index()
    industry_salary.columns = ['Industry', 'Average Salary']

    fig = px.bar(
        industry_salary,
        x="Average Salary",
        y="Industry",
        labels={"Average Salary": "Average Salary", "Industry": "Industry"},
        title="Average Salary by Industry"
    )
    st.plotly_chart(fig, key=uuid.uuid4())

def remote_vs_onsite(df):
    df["remote_type"] = df["remote_ratio"].map({
    0: "On-site",
    50: "Hybrid",
    100: "Remote"
    })

    remote_salary = df.groupby("remote_type")["salary_usd"].mean()
    remote_salary = remote_salary.reset_index()
    remote_salary.columns = ['Remote Type', 'Average Salary']

    fig = px.bar(
        remote_salary,
        x="Remote Type",
        y="Average Salary",
        labels={"Remote Type": "Remote Type", "Average Salary": "Average Salary"},
        title="Average Salary by Remote Type"
    )
    st.plotly_chart(fig, key=uuid.uuid4())

def top_ten_skills(df, skills_col="required_skills"):
    # Explode list of skills into separate rows
    df[skills_col] = df[skills_col].str.lower().str.split(", ")

    df_exploded = df.explode(skills_col)
    skill_salary = df_exploded.groupby(skills_col)["salary_usd"].mean().sort_values(ascending=False)

    skill_salary.columns = ["Skill", "Average Salary"]
    skill_salary = skill_salary.sort_values().tail(10)
    
    # Plot
    fig = px.bar(
        skill_salary,
        y=skill_salary.index,
        x=skill_salary.values,
        labels={"required_skills": "Skills", "x": "Average Salary"},
        title="Top 10 Highest Paying Skills"
    )
    st.plotly_chart(fig, key=uuid.uuid4())


# def top_ten_skills(df, skills_col="required_skills"):
#     # Explode list of skills into separate rows
#     skills_df = df.explode(skills_col)
    
#     # Count occurrences of each skill
#     top_skills = (
#         skills_df[skills_col]
#         .value_counts()
#         .head(10)
#         .reset_index()
#     )
#     top_skills.columns = ["Skill", "Count"]
    
#     # Plot
#     fig = px.bar(
#         top_skills,
#         x="Skill",
#         y="Count",
#         labels={"Skill": "Skill", "Count": "Frequency"},
#         title="Top 10 Required Skills"
#     )
#     st.plotly_chart(fig, key=uuid.uuid4())
