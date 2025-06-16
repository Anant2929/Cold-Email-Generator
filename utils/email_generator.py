from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_groq import ChatGroq
import chromadb
from chromadb.config import Settings
import pandas as pd
import uuid
from utils.job_extractor import extract_job_info
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

chroma_client = chromadb.PersistentClient(
    path="/mount/tmp/chroma_db",  
    settings=Settings(anonymized_telemetry=False)
)

llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"],
    model_name="llama3-70b-8192"
)

email_prompt = ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template("""
    You're an AI assistant helping a candidate write a cold email to apply for a job.

    Job Role: {role}  
    Experience Required: {experience}  
    Skills Required: {skills}  
    Description: {description}  
    Portfolio Links: {links}

    Write a cold email with a subject line. Be concise, confident, and professional.
    """)
])

def generate_email(job_url: str) -> str:
    job = extract_job_info(job_url)

    df = pd.read_csv("data/my_portfolio.csv")

    client = chromadb.PersistentClient(path='vectorstore')
    collection = client.get_or_create_collection(name="portfolio")

    if collection.count() == 0:
        for _, row in df.iterrows():
            collection.add(
                documents=[row["Techstack"]],
                metadatas=[{"link": row["Links"]}],
                ids=[str(uuid.uuid4())]
            )

    results = collection.query(query_texts=[" ".join(job['skills'])], n_results=2)
    matched_links = [item['link'] for item in results['metadatas'][0]]

    email_chain = email_prompt | llm
    output = email_chain.invoke({
        "role": job['role'],
        "experience": job['experience'],
        "skills": job['skills'],
        "description": job['description'],
        "links": ", ".join(matched_links)
    })

    return output.content
