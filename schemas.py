from pydantic import BaseModel, Field
from typing import List, Optional

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
    intent: str = "continue"  # continue|flirt|deflect|exit
    tone: str = "wholesome"

class ReplyOption(BaseModel):
    reply: str
    vibe_level: str  # low|medium|high
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
