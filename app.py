import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
import time
from datetime import datetime
from schemas import (
    GenerateBioIn, OpenerIn, ReplyIn, 
    DatePlanIn, RedFlagIn, RoastIn,
    ScreenshotAnalysisIn, ConversationScreenshotIn
)
from mcp_server import (
    generate_bio, opener, reply, 
    date_plan, red_flag_check, profile_roast,
    analyze_profile_screenshot, analyze_conversation_screenshot
)

load_dotenv()
APP_NAME = os.getenv("APP_NAME", "AI Wingman MCP")

app = FastAPI(
    title="AI Wingman MCP Server", 
    description="Dating app wingman tools with screenshot analysis for Puch AI",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for web requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional: Request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"{datetime.now()}: {request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s")
    return response

@app.get("/")
async def root():
    return {
        "status": "ok", 
        "app": APP_NAME,
        "description": "AI Wingman MCP Server for Puch AI",
        "version": "2.0.0",
        "features": [
            "Bio generation",
            "Conversation openers",
            "Reply suggestions", 
            "Date planning",
            "Safety checks",
            "Profile roasting",
            "Screenshot analysis",
            "Conversation analysis"
        ],
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "mcp": "/mcp",
            "generate_bio": "/bio",
            "opener": "/opener", 
            "reply": "/reply",
            "date_plan": "/date-plan",
            "red_flag_check": "/safety",
            "profile_roast": "/roast",
            "profile_screenshot": "/analyze-profile",
            "conversation_screenshot": "/analyze-conversation"
        },
        "integration": "Ready for Puch AI MCP integration",
        "deployment": {
            "platform": "Render",
            "status": "Production Ready"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "service": "ai-wingman-v2",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

# NEW: MCP Protocol Endpoints for Puch AI Integration
@app.get("/mcp")
async def mcp_info():
    """MCP server information for Puch AI discovery"""
    return {
        "name": "ai-wingman-mcp",
        "version": "2.0.0",
        "description": "AI Wingman for dating app assistance with screenshot analysis",
        "server_url": "https://dating-wingman.onrender.com",
        "protocol": "mcp",
        "tools": [
            {
                "name": "generate_bio",
                "description": "Generate improved dating app bios based on user interests and personality",
                "endpoint": "/bio",
                "method": "POST",
                "parameters": ["profile_text", "tone", "length", "app"]
            },
            {
                "name": "opener",
                "description": "Generate personalized conversation openers based on profile analysis", 
                "endpoint": "/opener",
                "method": "POST",
                "parameters": ["their_profile_text", "tone", "count"]
            },
            {
                "name": "reply",
                "description": "Generate thoughtful conversation replies to continue conversations",
                "endpoint": "/reply",
                "method": "POST",
                "parameters": ["partner_msg", "intent", "tone"]
            },
            {
                "name": "date_plan",
                "description": "Generate personalized first date plans based on location and interests",
                "endpoint": "/date-plan",
                "method": "POST",
                "parameters": ["city", "budget", "interests", "vibe"]
            },
            {
                "name": "red_flag_check",
                "description": "Analyze profiles for potential red flags and safety concerns",
                "endpoint": "/safety",
                "method": "POST",
                "parameters": ["profile_text"]
            },
            {
                "name": "profile_roast",
                "description": "Provide constructive feedback on dating profiles with humor",
                "endpoint": "/roast",
                "method": "POST",
                "parameters": ["bio", "images_desc"]
            },
            {
                "name": "analyze_profile_screenshot",
                "description": "Analyze dating profile screenshots using AI Vision and generate personalized openers",
                "endpoint": "/analyze-profile",
                "method": "POST",
                "parameters": ["image_data", "analysis_type", "context"]
            },
            {
                "name": "analyze_conversation_screenshot",
                "description": "Analyze conversation screenshots and suggest intelligent replies", 
                "endpoint": "/analyze-conversation",
                "method": "POST",
                "parameters": ["image_data", "my_role", "context"]
            }
        ],
        "authentication": {
            "type": "bearer_token",
            "valid_tokens": ["puch2024", "wingman123"]
        }
    }

@app.post("/mcp")
async def mcp_connect(data: dict = None):
    """MCP connection endpoint for Puch AI authentication"""
    try:
        token = None
        if data and isinstance(data, dict):
            token = data.get("token") or data.get("bearer_token")
        
        # Check if token is valid
        valid_tokens = ["puch2024", "wingman123"]
        token_valid = token in valid_tokens if token else False
        
        return {
            "status": "connected" if token_valid else "authentication_required",
            "server": "ai-wingman-mcp",
            "version": "2.0.0",
            "token_valid": token_valid,
            "connection_id": f"conn_{int(time.time())}",
            "capabilities": [
                "bio_generation",
                "conversation_analysis", 
                "screenshot_processing",
                "safety_checking",
                "date_planning"
            ],
            "message": "AI Wingman MCP server ready for dating assistance" if token_valid else "Please provide valid bearer token"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Connection failed: {str(e)}"
        }

# Core dating wingman endpoints
@app.post("/bio")
async def bio_endpoint(input: GenerateBioIn):
    """Generate improved dating app bios"""
    try:
        result = await generate_bio(input)
        return result
    except Exception as e:
        print(f"Bio generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Bio generation failed: {str(e)}")

@app.post("/opener")
async def opener_endpoint(input: OpenerIn):
    """Generate conversation openers"""
    try:
        result = await opener(input)
        return result
    except Exception as e:
        print(f"Opener generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Opener generation failed: {str(e)}")

@app.post("/reply")
async def reply_endpoint(input: ReplyIn):
    """Generate conversation replies"""
    try:
        result = await reply(input)
        return result
    except Exception as e:
        print(f"Reply generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Reply generation failed: {str(e)}")

@app.post("/date-plan")
async def date_plan_endpoint(input: DatePlanIn):
    """Generate date plans"""
    try:
        result = await date_plan(input)
        return result
    except Exception as e:
        print(f"Date plan generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Date plan generation failed: {str(e)}")

@app.post("/safety")
async def safety_endpoint(input: RedFlagIn):
    """Check for red flags"""
    try:
        result = await red_flag_check(input)
        return result
    except Exception as e:
        print(f"Safety check error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Safety check failed: {str(e)}")

@app.post("/roast")
async def roast_endpoint(input: RoastIn):
    """Profile roast and feedback"""
    try:
        result = await profile_roast(input)
        return result
    except Exception as e:
        print(f"Profile roast error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Profile roast failed: {str(e)}")

# Screenshot analysis endpoints
@app.post("/analyze-profile")
async def analyze_profile_endpoint(input: ScreenshotAnalysisIn):
    """Analyze dating profile screenshots and generate openers"""
    try:
        result = await analyze_profile_screenshot(input)
        return result
    except Exception as e:
        print(f"Profile screenshot analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Profile analysis failed: {str(e)}")

@app.post("/analyze-conversation")
async def analyze_conversation_endpoint(input: ConversationScreenshotIn):
    """Analyze conversation screenshots and suggest replies"""
    try:
        result = await analyze_conversation_screenshot(input)
        return result
    except Exception as e:
        print(f"Conversation screenshot analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Conversation analysis failed: {str(e)}")

# Additional utility endpoints
@app.get("/status")
async def status():
    """Extended status information"""
    return {
        "server_status": "running",
        "ai_model": os.getenv("OPENAI_MODEL", "gpt-4o"),
        "features_enabled": [
            "bio_generation",
            "conversation_openers", 
            "reply_suggestions",
            "date_planning",
            "safety_checks",
            "profile_roasting",
            "screenshot_analysis"
        ],
        "integration_ready": True,
        "puch_ai_compatible": True,
        "mcp_protocol": "enabled"
    }

@app.get("/tools")
async def list_tools():
    """List all available AI wingman tools"""
    return {
        "tools": [
            {
                "name": "generate_bio",
                "endpoint": "/bio",
                "description": "Generate improved dating app bios",
                "input": "profile_text, tone, length, app"
            },
            {
                "name": "opener",
                "endpoint": "/opener", 
                "description": "Generate conversation openers",
                "input": "their_profile_text, tone, count"
            },
            {
                "name": "reply",
                "endpoint": "/reply",
                "description": "Generate conversation replies", 
                "input": "partner_msg, intent, tone"
            },
            {
                "name": "date_plan",
                "endpoint": "/date-plan",
                "description": "Generate date plans",
                "input": "city, budget, interests, vibe"
            },
            {
                "name": "safety_check", 
                "endpoint": "/safety",
                "description": "Check for red flags",
                "input": "profile_text"
            },
            {
                "name": "profile_roast",
                "endpoint": "/roast",
                "description": "Profile feedback with humor",
                "input": "bio, images_desc"
            },
            {
                "name": "analyze_profile_screenshot",
                "endpoint": "/analyze-profile",
                "description": "Analyze dating profile screenshots",
                "input": "image_data, analysis_type, context"
            },
            {
                "name": "analyze_conversation_screenshot",
                "endpoint": "/analyze-conversation", 
                "description": "Analyze conversation screenshots",
                "input": "image_data, my_role, context"
            }
        ]
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
