from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"]

llm = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768", api_key=groq_api_key)

template = """Extract key details from the following job post. Return the output in this format:
Job Title: ...
Company: ...
Key Requirements: ...
Tech Stack: ...

Job Posting:
{job_posting}
"""

prompt = ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template(template)
])

chain = prompt | llm

def extract_job_info(job_posting: str) -> str:
    return chain.invoke({"job_posting": job_posting}).content
