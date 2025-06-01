# openai_config.py
# Loads your OpenAI API key and model securely from environment variables using python-dotenv
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "o4-mini")  # fallback default
