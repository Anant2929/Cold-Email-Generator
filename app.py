import streamlit as st
from utils.job_extractor import extract_job_info
from utils.email_generator import generate_email

st.set_page_config(page_title="Cold Email Generator", layout="centered")
st.title("📧 Cold Email Generator using LLM")

url = st.text_input("Paste Job Posting URL:")
if st.button("Generate Cold Email"):
    with st.spinner("Scraping and generating email..."):
        try:
            email_output = generate_email(url)
            st.success("Here's your cold email:")
            st.text_area("Cold Email", email_output, height=300)
        except Exception as e:
            st.error(f"❌ Error: {e}")
