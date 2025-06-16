import streamlit as st
from utils.job_extractor import extract_job_info
from utils.email_generator import generate_email

st.set_page_config(page_title="Cold Email Generator", layout="centered")
st.title("📧 Cold Email Generator using LLM")

with st.form("email_form"):
    job_posting_text = st.text_area("Paste the Job Posting Description Here")
    name = st.text_input("Your Name")
    role = st.text_input("Target Role (e.g. Software Engineer, Data Scientist)")
    skills = st.text_area("Your Key Skills (comma-separated)")
    experience = st.text_area("Your Relevant Experience (short paragraph)")

    submitted = st.form_submit_button("Generate Cold Email")

    if submitted:
        with st.spinner("Generating cold email..."):
            job_info = extract_job_info(job_posting_text)
            email = generate_email(name, role, skills, experience, job_info)
            st.success("Cold email generated!")
            st.text_area("✉️ Your Cold Email", value=email, height=300)
