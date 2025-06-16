from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_groq import ChatGroq
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"] 

llm = ChatGroq(temperature=0.7, model_name="mixtral-8x7b-32768", api_key=groq_api_key)

template = """
You are a skilled professional writing a cold email for a job.

Write a concise, friendly, and impactful cold email introducing the candidate to the recruiter.

Details:
- Candidate Name: {name}
- Target Role: {role}
- Key Skills: {skills}
- Relevant Experience: {experience}
- Job Info: {job_info}

Don't include portfolio links. End the email in a polite, enthusiastic tone, and request for a quick chat if the opportunity aligns.
"""

prompt = ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template(template)
])

chain = prompt | llm

def generate_email(name, role, skills, experience, job_info) -> str:
    return chain.invoke({
        "name": name,
        "role": role,
        "skills": skills,
        "experience": experience,
        "job_info": job_info
    }).content
