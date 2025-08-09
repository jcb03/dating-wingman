import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
from openai import AsyncOpenAI
import base64

# Load .env BEFORE reading environment variables
load_dotenv()

# Check if API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set. Make sure .env file exists and contains the API key.")

client = AsyncOpenAI(api_key=api_key)
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")  # Use gpt-4o for vision capabilities

SYSTEM = """You are a respectful, ethical AI wingman.
- Keep language friendly, playful, and non-manipulative.
- Do not produce explicit content or harassment.
- Encourage consent, safety, and clear boundaries.
- Be culturally aware and adaptable for Gen Z.
- Keep outputs WhatsApp-friendly (short paragraphs, bullets when needed).
"""

async def chat(messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
    """Standard text-only chat"""
    resp = await client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=temperature,
        messages=[{"role": "system", "content": SYSTEM}] + messages,
    )
    return resp.choices[0].message.content

async def analyze_image_with_text(image_base64: str, prompt: str, temperature: float = 0.7) -> str:
    """Analyze image with vision model"""
    try:
        # Ensure we're using a vision-capable model
        vision_model = "gpt-4o" if "gpt-4" in OPENAI_MODEL else "gpt-4o"
        
        messages = [
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ]
        
        resp = await client.chat.completions.create(
            model=vision_model,
            temperature=temperature,
            messages=messages,
            max_tokens=1000
        )
        
        return resp.choices[0].message.content
        
    except Exception as e:
        # Fallback to text-only analysis if vision fails
        fallback_prompt = f"{prompt}\n\nNote: Image analysis failed, please provide text description: {str(e)}"
        return await chat([{"role": "user", "content": fallback_prompt}], temperature)
