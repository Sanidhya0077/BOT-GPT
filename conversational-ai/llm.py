import os
from groq import Groq
from dotenv import load_dotenv
from fastapi import HTTPException
import logging

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
logger = logging.getLogger(__name__)

def call_llm(messages):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            timeout=30  # Add timeout to prevent hanging
        )
        return response.choices[0].message.content
    
    except Exception as e:
        # Log the actual error for debugging
        logger.error(f"LLM API error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="AI service temporarily unavailable"
        )
