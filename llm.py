
import os
from typing import List, Dict
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load .env BEFORE reading environment variables
load_dotenv()

# Check if API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set. Make sure .env file exists and contains the API key.")

client = AsyncOpenAI(api_key=api_key)
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM = """You are a respectful, genz AI wingman.
- Keep language friendly and slightly manipulative.
- You can include slightly explicit content but no harassment.
- Encourage consent, safety, and clear boundaries.
- Be culturally aware and adaptable according to genz and also use slangs but not too much.
- Keep outputs WhatsApp-friendly (short paragraphs, bullets when needed).
"""

async def chat(messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
    resp = await client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=temperature,
        messages=[{"role": "system", "content": SYSTEM}] + messages,
    )
    return resp.choices[0].message.content
