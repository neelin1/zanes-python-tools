# shared/gemini/client.py
import os
import google.genai as genai
from dotenv import load_dotenv

# Global client instance
_gemini_client = None


def initialize_gemini():
    """
    Initializes and returns a global Gemini client.
    """
    global _gemini_client
    if _gemini_client is None:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in .env file or environment variables."
            )
        # In the new API, the client is initialized with the key
        _gemini_client = genai.Client(api_key=api_key)
    return _gemini_client
