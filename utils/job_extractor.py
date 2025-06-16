from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
import json
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-70b-8192"
)

prompt_extract = ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template("""
    ### SCRAPED TEXT FROM WEBSITE:
    {page_data}
    ### INSTRUCTION:
    The scraped text is from the career's page of a website.
    Your job is to extract the job postings and return them in JSON format containing the 
    following keys: `role`, `experience`, `skills`, and `description`.
    Only return the valid JSON. No explanation or additional text.
    """)
])

def extract_job_info(url: str) -> dict:
    if not url.startswith("http"):
        url = "https://" + url
    loader = WebBaseLoader(url)
    page_data = loader.load()[0].page_content
    chain = prompt_extract | llm
    response = chain.invoke({"page_data": page_data})
    parsed = json.loads(response.content)
    return parsed[0] if isinstance(parsed, list) else parsed
