import base64
import io
from PIL import Image
from typing import Dict, Any

class ImageProcessor:
    def __init__(self):
        pass
    
    def decode_base64_image(self, base64_data: str) -> Image.Image:
        """Convert base64 string to PIL Image"""
        try:
            # Remove data URL prefix if present
            if base64_data.startswith('data:image'):
                base64_data = base64_data.split(',')[1]
            
            # Decode base64
            image_bytes = base64.b64decode(base64_data)
            image = Image.open(io.BytesIO(image_bytes))
            return image
        except Exception as e:
            raise ValueError(f"Failed to decode image: {str(e)}")
    
    def extract_text_from_image(self, image: Image.Image) -> str:
        """Skip OCR - let OpenAI Vision handle text extraction"""
        return "Text extraction handled by AI Vision API"
    
    def extract_profile_data(self, text: str) -> Dict[str, Any]:
        """Return empty profile data - AI Vision will handle extraction"""
        return {
            "name": None,
            "age": None,
            "bio": None,
            "interests": [],
            "education": None,
            "work": None,
            "location": None
        }

# Initialize global processor
image_processor = ImageProcessor()
