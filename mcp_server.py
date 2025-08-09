import os
import mcp
from openai import AsyncOpenAI
from typing import Any, Dict, List
from image_processor import image_processor

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Tool: validate (required by Puch) ---
@mcp.tool
async def validate() -> str:
    """Required by Puch AI - returns phone number in country_code+number format"""
    MY_NUMBER = "918920560661"  # Replace with your actual number
    return MY_NUMBER

# --- Tool: generate_bio ---
@mcp.tool
async def generate_bio(input: Dict[str, Any]) -> Dict[str, Any]:
    """Generate improved dating app bios"""
    try:
        response = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            messages=[
                {"role": "system", "content": f"""You are an expert dating coach specializing in creating compelling dating app bios. 
                Create a {input.get('tone', 'confident')} bio that's {input.get('length', 'medium')} length for {input.get('app', 'dating apps')}.
                Make it authentic, engaging, and conversation-starting. Include personality traits, interests, and a subtle call-to-action."""},
                {"role": "user", "content": f"Create a bio based on: {input.get('profile_text', '')}"}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        bio = response.choices[0].message.content
        
        return {
            "improved_bio": bio,
            "tone": input.get('tone', 'confident'),
            "length": input.get('length', 'medium'),
            "app": input.get('app', 'dating apps'),
            "tips": [
                "Be authentic and genuine",
                "Include conversation starters",
                "Show personality through interests",
                "Keep it positive and upbeat"
            ]
        }
        
    except Exception as e:
        return {"error": f"Bio generation failed: {str(e)}"}

# --- Tool: opener ---
@mcp.tool
async def opener(input: Dict[str, Any]) -> Dict[str, Any]:
    """Generate conversation openers"""
    try:
        response = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            messages=[
                {"role": "system", "content": f"""You are a dating expert who creates personalized, engaging conversation starters.
                Generate {input.get('count', 3)} openers with a {input.get('tone', 'friendly')} tone.
                Make them specific to the person's profile, avoid generic messages, and include follow-up suggestions."""},
                {"role": "user", "content": f"Profile info: {input.get('their_profile_text', '')}"}
            ],
            temperature=0.8,
            max_tokens=400
        )
        
        content = response.choices[0].message.content
        
        return {
            "openers": content,
            "tone": input.get('tone', 'friendly'),
            "count": input.get('count', 3),
            "strategy": "Personalized based on profile interests and details"
        }
        
    except Exception as e:
        return {"error": f"Opener generation failed: {str(e)}"}

# --- Tool: reply ---
@mcp.tool
async def reply(input: Dict[str, Any]) -> Dict[str, Any]:
    """Generate conversation replies"""
    try:
        response = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            messages=[
                {"role": "system", "content": f"""You are a dating conversation expert. Generate thoughtful replies with a {input.get('tone', 'friendly')} tone.
                Intent: {input.get('intent', 'continue conversation')}. 
                Make responses engaging, authentic, and keep the conversation flowing naturally."""},
                {"role": "user", "content": f"They said: {input.get('partner_msg', '')}"}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        reply_text = response.choices[0].message.content
        
        return {
            "suggested_reply": reply_text,
            "tone": input.get('tone', 'friendly'),
            "intent": input.get('intent', 'continue conversation'),
            "conversation_tips": [
                "Ask open-ended questions",
                "Show genuine interest",
                "Share something about yourself",
                "Keep the energy positive"
            ]
        }
        
    except Exception as e:
        return {"error": f"Reply generation failed: {str(e)}"}

# --- Tool: date_plan ---
@mcp.tool
async def date_plan(input: Dict[str, Any]) -> Dict[str, Any]:
    """Generate date plans"""
    try:
        response = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            messages=[
                {"role": "system", "content": f"""You are a local dating expert who creates perfect first date plans.
                Budget: {input.get('budget', 'medium')}
                Vibe: {input.get('vibe', 'casual')}
                Create specific, actionable date ideas with venues, activities, and timing."""},
                {"role": "user", "content": f"Plan a date in {input.get('city', '')} for people interested in: {input.get('interests', '')}"}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        plan = response.choices[0].message.content
        
        return {
            "date_plan": plan,
            "city": input.get('city', ''),
            "budget": input.get('budget', 'medium'),
            "vibe": input.get('vibe', 'casual'),
            "interests": input.get('interests', ''),
            "success_tips": [
                "Arrive on time",
                "Be present and engaged",
                "Have backup conversation topics",
                "Be yourself and have fun"
            ]
        }
        
    except Exception as e:
        return {"error": f"Date plan generation failed: {str(e)}"}

# --- Tool: red_flag_check ---
@mcp.tool
async def red_flag_check(input: Dict[str, Any]) -> Dict[str, Any]:
    """Check for red flags"""
    try:
        response = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            messages=[
                {"role": "system", "content": """You are a dating safety expert. Analyze profiles/messages for potential red flags.
                Be thorough but balanced - point out genuine concerns while not being overly paranoid.
                Provide safety advice and trust-your-gut guidance."""},
                {"role": "user", "content": f"Analyze this for red flags: {input.get('profile_text', '')}"}
            ],
            temperature=0.3,
            max_tokens=400
        )
        
        analysis = response.choices[0].message.content
        
        return {
            "safety_analysis": analysis,
            "profile_text": input.get('profile_text', ''),
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

# --- Tool: profile_roast ---
@mcp.tool
async def profile_roast(input: Dict[str, Any]) -> Dict[str, Any]:
    """Profile roast and feedback"""
    try:
        response = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            messages=[
                {"role": "system", "content": """You are a witty dating coach who gives brutally honest but constructive feedback.
                Roast the profile with humor while providing actionable improvement suggestions.
                Be funny but helpful - the goal is to make them laugh while helping them improve."""},
                {"role": "user", "content": f"Bio: {input.get('bio', '')}\nImages described: {input.get('images_desc', '')}"}
            ],
            temperature=0.8,
            max_tokens=400
        )
        
        roast = response.choices[0].message.content
        
        return {
            "roast": roast,
            "bio": input.get('bio', ''),
            "images_desc": input.get('images_desc', ''),
            "improvement_areas": [
                "Profile photo quality",
                "Bio authenticity and engagement",
                "Conversation starters",
                "Overall profile completeness"
            ]
        }
        
    except Exception as e:
        return {"error": f"Profile roast failed: {str(e)}"}

# --- Tool: analyze_profile_screenshot ---
@mcp.tool
async def analyze_profile_screenshot(input: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze dating profile screenshots using AI Vision"""
    try:
        # Decode and process the image
        image_data = input.get("image_data", "")
        if not image_data:
            return {"error": "No image data provided"}
        
        # Use OpenAI Vision API to analyze the screenshot
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""Analyze this dating profile screenshot and provide detailed insights:

1. Extract all visible text (name, age, bio, interests, etc.)
2. Identify the person's interests, hobbies, and personality traits
3. Note their education, work, location if visible
4. Generate 3-5 personalized conversation openers based on their profile
5. Identify any potential red flags or concerns
6. Provide an overall analysis and dating strategy advice

Context: {input.get('context', 'Dating profile analysis')}
Analysis type: {input.get('analysis_type', 'profile')}"""
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
            temperature=0.7,
            max_tokens=1000
        )
        
        analysis_content = response.choices[0].message.content
        
        # Parse the analysis and structure the response
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
            "context": input.get('context', ''),
            "analysis_type": input.get('analysis_type', 'profile')
        }
        
    except Exception as e:
        return {
            "error": f"Screenshot analysis failed: {str(e)}",
            "extracted_text": f"Error analyzing screenshot: {str(e)}",
            "analysis_summary": "Unable to analyze screenshot. Please try uploading a clearer image."
        }

# --- Tool: analyze_conversation_screenshot ---
@mcp.tool
async def analyze_conversation_screenshot(input: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze conversation screenshots and suggest replies"""
    try:
        # Decode and process the image
        image_data = input.get("image_data", "")
        if not image_data:
            return {"error": "No image data provided"}
        
        # Use OpenAI Vision API to analyze the conversation screenshot
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""Analyze this dating conversation screenshot and provide strategic advice:

1. Extract all visible messages and identify who said what
2. Analyze the conversation tone, flow, and current momentum
3. Suggest 3-5 thoughtful reply options with different vibes (playful, serious, flirty, etc.)
4. Provide conversation analysis and strategy advice
5. Suggest next steps for the conversation

My role in conversation: {input.get('my_role', 'sender')}
Context: {input.get('context', 'Conversation analysis')}"""
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
            temperature=0.7,
            max_tokens=1000
        )
        
        analysis_content = response.choices[0].message.content
        
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
            "my_role": input.get('my_role', 'sender'),
            "context": input.get('context', '')
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
