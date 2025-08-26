import streamlit as st

st.title("AI Job Prediction App")
st.header("Welcome to the AI Job Prediction App!")

st.markdown("""
This is a tool that helps you:
- 📊 Predict salaries for single job postings
- 📂 Upload a batch of jobs to analyze at once
- 📈 Explore market insights such as top-paying skills, industries, and remote trends
""")

st.subheader("Get Started with:")

col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/Job_Prediction.py", label="🔮 Job Prediction")
with col2:
    st.page_link("pages/Batch_Upload.py", label="📂 Batch Upload")
with col3:
    st.page_link("pages/Dashboard.py", label="📊 Dashboard")


footer_html = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    color: gray;
    padding: 10px;
    font-size: 14px;
    border-top: 0.5px solid #e6e6e6; /* Optional top border */
    
}

.divs {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
<div class="footer">
    <div class="divs">
        <p style="margin-left: 100px;">Developed with Streamlit by ML Group 3</p>
    </div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)