import os

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    api_key = st.secrets.get("GROQ_API_KEY")

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=api_key
)