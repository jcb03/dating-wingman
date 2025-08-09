import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import uvicorn
from schemas import (
    GenerateBioIn, OpenerIn, ReplyIn, 
    DatePlanIn, RedFlagIn, RoastIn
)
from mcp_server import (
    generate_bio, opener, reply, 
    date_plan, red_flag_check, profile_roast
)

load_dotenv()
APP_NAME = os.getenv("APP_NAME", "Dating Wingman")

app = FastAPI(
    title="AI Wingman API", 
    description="Dating app wingman tools",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "status": "ok", 
        "app": APP_NAME,
        "description": "AI Wingman - Dating App Assistant",
        "endpoints": {
            "generate_bio": "/bio",
            "opener": "/opener", 
            "reply": "/reply",
            "date_plan": "/date-plan",
            "red_flag_check": "/safety",
            "profile_roast": "/roast"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "ai-wingman"}

@app.post("/bio")
async def bio_endpoint(input: GenerateBioIn):
    """Generate improved dating app bios"""
    try:
        return await generate_bio(input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/opener")
async def opener_endpoint(input: OpenerIn):
    """Generate conversation openers"""
    try:
        return await opener(input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reply")
async def reply_endpoint(input: ReplyIn):
    """Generate conversation replies"""
    try:
        return await reply(input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/date-plan")
async def date_plan_endpoint(input: DatePlanIn):
    """Generate date plans"""
    try:
        return await date_plan(input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/safety")
async def safety_endpoint(input: RedFlagIn):
    """Check for red flags"""
    try:
        return await red_flag_check(input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/roast")
async def roast_endpoint(input: RoastIn):
    """Profile roast and feedback"""
    try:
        return await profile_roast(input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
