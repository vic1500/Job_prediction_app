import streamlit as st

home_page = st.Page("pages/Home.py", title="Home", icon=":material/home:")
job_prediction_page = st.Page("pages/Job_Prediction.py", title="Job Prediction", icon=":material/business_center:")
dashboard_page = st.Page("pages/Dashboard.py", title="Dashboard", icon=":material/analytics:")
batch_upload_page = st.Page("pages/Batch_Upload.py", title="Batch Upload", icon=":material/batch_prediction:")

pg = st.navigation([home_page, job_prediction_page, dashboard_page, batch_upload_page])
st.set_page_config(page_title="AI Job Prediction app", page_icon=":material/robot:")
pg.run()
