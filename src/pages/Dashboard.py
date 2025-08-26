import streamlit as st
import pandas as pd
from utils.plot_utils import plot_bar_chart, top_ten_skills, salary_by_industry, remote_vs_onsite

st.title("📊 Dashboard")
st.header("Explore the Job Market Data")

tab1, tab2 = st.tabs(["Job Market Data", "Your Data"])

df = pd.read_csv("data/ai_job_dataset.csv")

with tab1:
    st.subheader("Job Market Data Overview")
    plot_bar_chart(df, x="job_title", y="salary_usd", title="Average Salary by Job Title", xlabel="Salary in USD", ylabel="Job Role")
    top_ten_skills(df)
    salary_by_industry(df)
    remote_vs_onsite(df)

    show_data = st.checkbox("Show Raw Data")
    if show_data:
        st.dataframe(df)
        summary_stats_col, include_col = st.columns(2)
        with summary_stats_col:
            show_summary = st.checkbox("Show Summary Statistics")
        with include_col:
            include = st.selectbox("Include", options=["All", "Numerical", "Object"]).lower()
        if show_summary:
            transpose = st.checkbox("Transpose", value=True)
            st.write("Summary Statistics:")
            if transpose:
                st.dataframe(df.describe(include=None if include == "numerical" else include).T)
            else:
                st.dataframe(df.describe(include=None if include == "numerical" else include))

with tab2:
    csv = st.file_uploader("Upload your CSV file for visualization", type=["csv"])
    if csv:
        st.subheader("Your Data Insights")
        user_data = pd.read_csv(csv)

        plot_bar_chart(user_data, x="job_title", y="salary_usd", title="Average Salary by Job Title")
        top_ten_skills(user_data)
        salary_by_industry(user_data)
        remote_vs_onsite(user_data)

        show_data = st.checkbox("Show Raw Data", key="user_data")
        if show_data:
            st.write("Your Uploaded Data:")
            st.dataframe(user_data)
            summary_stats_col, include_col = st.columns(2)
        with summary_stats_col:
            show_summary = st.checkbox("Show Summary Statistics", key="user_data_summary")
        with include_col:
            include = st.selectbox("Include", options=["All", "Numerical", "Object"], key="user_data_include").lower()
        if show_summary:
            transpose = st.checkbox("Transpose", value=True, key="user_data_transpose")
            st.write("Summary Statistics:")
            if transpose:
                st.dataframe(user_data.describe(include=None if include == "numerical" else include).T)
            else:
                st.dataframe(user_data.describe(include=None if include == "numerical" else include))
    # Add visualizations or data insights related to the user's uploaded data
