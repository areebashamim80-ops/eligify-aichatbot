from fastapi import APIRouter
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

# Load .env for local development
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

# Read API key from Render Environment Variables or .env
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY not found. Please set it in Render Environment Variables or backend/.env"
    )

router = APIRouter(
    prefix="/ai",
    tags=["Eligify AI"]
)

client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
You are Eligify AI, an AI assistant for marginalized entrepreneurs.

Help entrepreneurs understand government schemes,
business opportunities, eligibility requirements,
documents and application guidance.

Be helpful, simple and clear.

Do not invent government schemes, eligibility rules,
benefits, documents, deadlines or application links.

When verified scheme data is not available,
clearly say that scheme-specific information needs
to be verified from official sources.
"""

@router.post("/chat")
def chat(message: str):
    try:
        response = client.responses.create(
            model="gpt-5.6",
            instructions=SYSTEM_PROMPT,
            input=message
        )

        return {
            "reply": response.output_text,
            "status": "success"
        }

    except Exception as error:
        return {
            "reply": f"AI ERROR: {str(error)}",
            "status": "error"
        }