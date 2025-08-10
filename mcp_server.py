import os
import asyncio
from typing import Any, Dict, List
from fastmcp import FastMCP
from dotenv import load_dotenv
from llm import LLMClient
from auth import verify_bearer_token
from image_processor import ImageProcessor

# Load environment variables
load_dotenv()

# Initialize components
llm = LLMClient()
image_processor = ImageProcessor()

# Initialize FastMCP server
mcp = FastMCP("AI Wingman MCP")

# Bearer token for authentication
BEARER_TOKEN = os.getenv("MCP_BEARER_TOKEN", "puch2024")

@mcp.tool()
async def validate() -> str:
    """Required by Puch AI - returns phone number in country_code+number format"""
    MY_NUMBER = "918920560661"  # Replace with your actual number
    return MY_NUMBER

@mcp.tool()
async def generate_bio(
    profile_text: str,
    tone: str = "confident",
    length: str = "medium",
    app: str = "tinder"
) -> Dict[str, Any]:
    """Generate improved dating app bios"""
    try:
        prompt = f"""You are an expert dating coach specializing in creating compelling dating app bios. 
        Create a {tone} bio that's {length} length for {app}.
        Make it authentic, engaging, and conversation-starting. Include personality traits, interests, and a subtle call-to-action.
        
        Create a bio based on: {profile_text}"""
        
        bio = await llm.generate_response(prompt, max_tokens=300, temperature=0.7)
        
        return {
            "improved_bio": bio,
            "tone": tone,
            "length": length,
            "app": app,
            "tips": [
                "Be authentic and genuine",
                "Include conversation starters",
                "Show personality through interests",
                "Keep it positive and upbeat"
            ]
        }
        
    except Exception as e:
        return {"error": f"Bio generation failed: {str(e)}"}

@mcp.tool()
async def opener(
    their_profile_text: str,
    tone: str = "friendly",
    count: int = 3
) -> Dict[str, Any]:
    """Generate conversation openers"""
    try:
        prompt = f"""You are a dating expert who creates personalized, engaging conversation starters.
        Generate {count} openers with a {tone} tone.
        Make them specific to the person's profile, avoid generic messages, and include follow-up suggestions.
        
        Profile info: {their_profile_text}"""
        
        content = await llm.generate_response(prompt, max_tokens=400, temperature=0.8)
        
        return {
            "openers": content,
            "tone": tone,
            "count": count,
            "strategy": "Personalized based on profile interests and details"
        }
        
    except Exception as e:
        return {"error": f"Opener generation failed: {str(e)}"}

@mcp.tool()
async def reply(
    partner_msg: str,
    intent: str = "continue",
    tone: str = "friendly"
) -> Dict[str, Any]:
    """Generate conversation replies"""
    try:
        prompt = f"""You are a dating conversation expert. Generate thoughtful replies with a {tone} tone.
        Intent: {intent}. 
        Make responses engaging, authentic, and keep the conversation flowing naturally.
        
        They said: {partner_msg}"""
        
        reply_text = await llm.generate_response(prompt, max_tokens=200, temperature=0.7)
        
        return {
            "suggested_reply": reply_text,
            "tone": tone,
            "intent": intent,
            "conversation_tips": [
                "Ask open-ended questions",
                "Show genuine interest",
                "Share something about yourself",
                "Keep the energy positive"
            ]
        }
        
    except Exception as e:
        return {"error": f"Reply generation failed: {str(e)}"}

@mcp.tool()
async def date_plan(
    city: str,
    budget: str = "medium",
    interests: str = "",
    vibe: str = "casual"
) -> Dict[str, Any]:
    """Generate date plans"""
    try:
        prompt = f"""You are a local dating expert who creates perfect first date plans.
        Budget: {budget}
        Vibe: {vibe}
        Create specific, actionable date ideas with venues, activities, and timing.
        
        Plan a date in {city} for people interested in: {interests}"""
        
        plan = await llm.generate_response(prompt, max_tokens=500, temperature=0.7)
        
        return {
            "date_plan": plan,
            "city": city,
            "budget": budget,
            "vibe": vibe,
            "interests": interests,
            "success_tips": [
                "Arrive on time",
                "Be present and engaged",
                "Have backup conversation topics",
                "Be yourself and have fun"
            ]
        }
        
    except Exception as e:
        return {"error": f"Date plan generation failed: {str(e)}"}

@mcp.tool()
async def red_flag_check(profile_text: str) -> Dict[str, Any]:
    """Check for red flags"""
    try:
        prompt = f"""You are a dating safety expert. Analyze profiles/messages for potential red flags.
        Be thorough but balanced - point out genuine concerns while not being overly paranoid.
        Provide safety advice and trust-your-gut guidance.
        
        Analyze this for red flags: {profile_text}"""
        
        analysis = await llm.generate_response(prompt, max_tokens=400, temperature=0.3)
        
        return {
            "safety_analysis": analysis,
            "profile_text": profile_text,
            "general_safety_tips": [
                "Meet in public places",
                "Tell friends about your plans",
                "Trust your instincts",
                "Video call before meeting",
                "Take your time getting to know them"
            ]
        }
        
    except Exception as e:
        return {"error": f"Safety check failed: {str(e)}"}

@mcp.tool()
async def profile_roast(
    bio: str,
    images_desc: str = ""
) -> Dict[str, Any]:
    """Profile roast and feedback"""
    try:
        prompt = f"""You are a witty dating coach who gives brutally honest but constructive feedback.
        Roast the profile with humor while providing actionable improvement suggestions.
        Be funny but helpful - the goal is to make them laugh while helping them improve.
        
        Bio: {bio}
        Images described: {images_desc}"""
        
        roast = await llm.generate_response(prompt, max_tokens=400, temperature=0.8)
        
        return {
            "roast": roast,
            "bio": bio,
            "images_desc": images_desc,
            "improvement_areas": [
                "Profile photo quality",
                "Bio authenticity and engagement",
                "Conversation starters",
                "Overall profile completeness"
            ]
        }
        
    except Exception as e:
        return {"error": f"Profile roast failed: {str(e)}"}

@mcp.tool()
async def analyze_profile_screenshot(
    image_data: str,
    analysis_type: str = "profile",
    context: str = ""
) -> Dict[str, Any]:
    """Analyze dating profile screenshots using AI Vision"""
    try:
        if not image_data:
            return {"error": "No image data provided"}
        
        # Decode and validate image
        image = image_processor.decode_base64_image(image_data)
        
        prompt = f"""Analyze this dating profile screenshot and provide detailed insights:

1. Extract all visible text (name, age, bio, interests, etc.)
2. Identify the person's interests, hobbies, and personality traits
3. Note their education, work, location if visible
4. Generate 3-5 personalized conversation openers based on their profile
5. Identify any potential red flags or concerns
6. Provide an overall analysis and dating strategy advice

Context: {context}
Analysis type: {analysis_type}"""
        
        analysis_content = await llm.analyze_image(image_data, prompt)
        
        return {
            "extracted_text": "Text extraction handled by AI Vision API",
            "profile_data": {
                "name": None,
                "age": None,
                "bio": None,
                "interests": [],
                "education": None,
                "work": None,
                "location": None
            },
            "suggested_openers": [
                {
                    "text": "Personalized opener based on AI Vision analysis",
                    "follow_ups": ["Follow up suggestion 1", "Follow up suggestion 2"],
                    "rationale": "Based on profile analysis"
                }
            ],
            "red_flags": [],
            "analysis_summary": analysis_content,
            "context": context,
            "analysis_type": analysis_type
        }
        
    except Exception as e:
        return {
            "error": f"Screenshot analysis failed: {str(e)}",
            "extracted_text": f"Error analyzing screenshot: {str(e)}",
            "analysis_summary": "Unable to analyze screenshot. Please try uploading a clearer image."
        }

@mcp.tool()
async def analyze_conversation_screenshot(
    image_data: str,
    my_role: str = "sender",
    context: str = ""
) -> Dict[str, Any]:
    """Analyze conversation screenshots and suggest replies"""
    try:
        if not image_data:
            return {"error": "No image data provided"}
        
        # Decode and validate image
        image = image_processor.decode_base64_image(image_data)
        
        prompt = f"""Analyze this dating conversation screenshot and provide strategic advice:

1. Extract all visible messages and identify who said what
2. Analyze the conversation tone, flow, and current momentum
3. Suggest 3-5 thoughtful reply options with different vibes (playful, serious, flirty, etc.)
4. Provide conversation analysis and strategy advice
5. Suggest next steps for the conversation

My role in conversation: {my_role}
Context: {context}"""
        
        analysis_content = await llm.analyze_image(image_data, prompt)
        
        return {
            "extracted_messages": [],
            "conversation_summary": analysis_content,
            "suggested_replies": [
                {
                    "reply": "Contextual reply suggestion based on AI analysis",
                    "vibe_level": "medium",
                    "boundary_safe_variant": "Alternative safe version",
                    "rationale": "Based on conversation flow analysis"
                }
            ],
            "conversation_analysis": "Analysis of conversation tone and momentum based on AI Vision",
            "next_step_advice": "Strategic advice for continuing the conversation",
            "my_role": my_role,
            "context": context
        }
        
    except Exception as e:
        return {
            "error": f"Conversation analysis failed: {str(e)}",
            "extracted_messages": [],
            "conversation_summary": f"Error analyzing conversation: {str(e)}",
            "suggested_replies": [],
            "conversation_analysis": "Unable to analyze conversation screenshot.",
            "next_step_advice": "Please try uploading a clearer image."
        }

# Set up authentication middleware
@mcp.middleware
async def auth_middleware(request, call_next):
    """Bearer token authentication middleware"""
    if not verify_bearer_token(request):
        # Allow unauthenticated access for MCP discovery endpoints
        if request.url.path in ["/", "/mcp", "/health"]:
            return await call_next(request)
        
        return {"error": "Unauthorized", "message": "Valid bearer token required"}
    
    return await call_next(request)

if __name__ == "__main__":
    # Run the MCP server
    port = int(os.getenv("PORT", 8000))
    print(f"Starting AI Wingman MCP Server on port {port}")
    print(f"Bearer token: {BEARER_TOKEN}")
    asyncio.run(mcp.run(port=port, host="0.0.0.0"))
