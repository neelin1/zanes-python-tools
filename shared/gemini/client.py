# shared/gemini_client.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

def initialize_gemini():
    """
    Initializes the Gemini client by loading the API key from the .env file
    and configuring the generative AI module.
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")
    genai.configure(api_key=api_key)
    return genai
