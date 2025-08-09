from pydantic import BaseModel, Field
from typing import List, Optional, Union
import base64

class GenerateBioIn(BaseModel):
    profile_text: str = Field(..., description="User's current bio/prompts/interests")
    tone: str = Field("playful", description="playful|witty|wholesome|flirty")
    length: str = Field("short", description="short|medium|long")
    app: str = Field("tinder", description="dating app name")

class BioSuggestion(BaseModel):
    text: str
    why_it_works: str
    dos: List[str]
    donts: List[str]

class GenerateBioOut(BaseModel):
    suggestions: List[BioSuggestion]

class OpenerIn(BaseModel):
    their_profile_text: str
    my_profile: Optional[str] = ""
    context: Optional[str] = ""
    tone: str = "witty"
    count: int = 5

class OpenerItem(BaseModel):
    text: str
    follow_ups: List[str]
    rationale: str

class OpenerOut(BaseModel):
    openers: List[OpenerItem]

class ReplyIn(BaseModel):
    partner_msg: str
    thread_context: Optional[str] = ""
    intent: str = "continue"
    tone: str = "wholesome"

class ReplyOption(BaseModel):
    reply: str
    vibe_level: str
    boundary_safe_variant: str
    rationale: str

class ReplyOut(BaseModel):
    options: List[ReplyOption]

class DatePlanIn(BaseModel):
    city: str
    budget: str
    interests: List[str]
    vibe: str
    duration_hours: int = 2

class DatePlan(BaseModel):
    title: str
    steps: List[str]
    opener_line: str
    rain_plan: Optional[str] = None
    booking_tips: List[str]

class DatePlanOut(BaseModel):
    plans: List[DatePlan]

class RedFlagIn(BaseModel):
    profile_text: str

class RedFlagItem(BaseModel):
    flag: str
    severity: str
    why: str
    boundary_statement: str

class RedFlagOut(BaseModel):
    items: List[RedFlagItem]

class RoastIn(BaseModel):
    bio: str
    images_desc: Optional[str] = ""

class RoastOut(BaseModel):
    roast: str
    reorder_advice: List[str]
    quick_fixes: List[str]

class ValidateIn(BaseModel):
    bearer_token: str = Field(..., description="Bearer token passed from Puch")

class ValidateOut(BaseModel):
    ok: bool
    user_id: Optional[str] = None

# NEW: Screenshot analysis schemas
class ScreenshotAnalysisIn(BaseModel):
    image_data: str = Field(..., description="Base64 encoded image data")
    analysis_type: str = Field("profile", description="profile|conversation|match")
    context: Optional[str] = Field("", description="Additional context about the screenshot")

class ExtractedProfileData(BaseModel):
    name: Optional[str] = None
    age: Optional[str] = None
    bio: Optional[str] = None
    interests: List[str] = []
    education: Optional[str] = None
    work: Optional[str] = None
    location: Optional[str] = None
    photos_description: Optional[str] = None

class ScreenshotAnalysisOut(BaseModel):
    extracted_text: str
    profile_data: Optional[ExtractedProfileData] = None
    suggested_openers: List[OpenerItem] = []
    red_flags: List[RedFlagItem] = []
    analysis_summary: str

class ConversationScreenshotIn(BaseModel):
    image_data: str = Field(..., description="Base64 encoded conversation screenshot")
    my_role: str = Field("sender", description="sender|receiver - which messages are mine")
    context: Optional[str] = Field("", description="Additional context")

class ConversationAnalysisOut(BaseModel):
    extracted_messages: List[dict]
    conversation_summary: str
    suggested_replies: List[ReplyOption]
    conversation_analysis: str
    next_step_advice: str
