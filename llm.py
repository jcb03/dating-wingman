import os
from typing import Optional, Dict, Any
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    """OpenAI LLM client for AI Wingman"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    async def generate_response(
        self, 
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        system_message: Optional[str] = None
    ) -> str:
        """Generate a text response using OpenAI"""
        try:
            messages = []
            
            if system_message:
                messages.append({"role": "system", "content": system_message})
            
            messages.append({"role": "user", "content": prompt})
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"LLM generation failed: {str(e)}")
    
    async def analyze_image(
        self, 
        image_data: str, 
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """Analyze an image using OpenAI Vision API"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o",  # Vision model
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Image analysis failed: {str(e)}")
    
    async def generate_structured_response(
        self, 
        prompt: str,
        response_format: Dict[str, Any],
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Generate a structured response using OpenAI with response format"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=response_format
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            # Fallback to regular text generation
            text_response = await self.generate_response(prompt, max_tokens, temperature)
            return {"content": text_response}
