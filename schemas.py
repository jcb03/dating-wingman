from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ValidateResponse(BaseModel):
    phone_number: str = Field(..., description="Phone number in country_code+number format")

class BioRequest(BaseModel):
    profile_text: str = Field(..., description="User's interests, personality, background")
    tone: str = Field("confident", description="confident|playful|serious|witty")
    length: str = Field("medium", description="short|medium|long")
    app: str = Field("tinder", description="tinder|bumble|hinge|other")

class BioResponse(BaseModel):
    improved_bio: str
    tone: str
    length: str
    app: str
    tips: List[str]

class OpenerRequest(BaseModel):
    their_profile_text: str = Field(..., description="Their profile information")
    tone: str = Field("friendly", description="friendly|playful|flirty|casual")
    count: int = Field(3, description="Number of openers to generate")

class OpenerResponse(BaseModel):
    openers: str
    tone: str
    count: int
    strategy: str

class ReplyRequest(BaseModel):
    partner_msg: str = Field(..., description="What they said")
    intent: str = Field("continue", description="continue|flirt|ask_out|deflect")
    tone: str = Field("friendly", description="friendly|playful|witty|serious")

class ReplyResponse(BaseModel):
    suggested_reply: str
    tone: str
    intent: str
    conversation_tips: List[str]

class DatePlanRequest(BaseModel):
    city: str = Field(..., description="City/location for the date")
    budget: str = Field("medium", description="low|medium|high")
    interests: str = Field("", description="Shared interests or activities")
    vibe: str = Field("casual", description="casual|romantic|adventurous|cultural")

class DatePlanResponse(BaseModel):
    date_plan: str
    city: str
    budget: str
    vibe: str
    interests: str
    success_tips: List[str]

class RedFlagRequest(BaseModel):
    profile_text: str = Field(..., description="Profile text or messages to analyze")

class RedFlagResponse(BaseModel):
    safety_analysis: str
    profile_text: str
    general_safety_tips: List[str]

class RoastRequest(BaseModel):
    bio: str = Field(..., description="Dating profile bio")
    images_desc: str = Field("", description="Description of profile images")

class RoastResponse(BaseModel):
    roast: str
    bio: str
    images_desc: str
    improvement_areas: List[str]

class ScreenshotAnalysisRequest(BaseModel):
    image_data: str = Field(..., description="Base64 encoded image data")
    analysis_type: str = Field("profile", description="profile|conversation|match")
    context: Optional[str] = Field("", description="Additional context")

class ConversationScreenshotRequest(BaseModel):
    image_data: str = Field(..., description="Base64 encoded conversation screenshot")
    my_role: str = Field("sender", description="sender|receiver")
    context: Optional[str] = Field("", description="Additional context")

class ExtractedProfileData(BaseModel):
    name: Optional[str] = None
    age: Optional[str] = None
    bio: Optional[str] = None
    interests: List[str] = []
    education: Optional[str] = None
    work: Optional[str] = None
    location: Optional[str] = None

class SuggestedOpener(BaseModel):
    text: str
    follow_ups: List[str] = []
    rationale: str

class ScreenshotAnalysisResponse(BaseModel):
    extracted_text: str
    profile_data: ExtractedProfileData
    suggested_openers: List[SuggestedOpener]
    red_flags: List[str] = []
    analysis_summary: str
    context: str = ""
    analysis_type: str = "profile"

class SuggestedReply(BaseModel):
    reply: str
    vibe_level: str
    boundary_safe_variant: str = ""
    rationale: str

class ConversationAnalysisResponse(BaseModel):
    extracted_messages: List[Dict[str, Any]] = []
    conversation_summary: str
    suggested_replies: List[SuggestedReply]
    conversation_analysis: str
    next_step_advice: str
    my_role: str = "sender"
    context: str = ""

class ErrorResponse(BaseModel):
    error: str
    message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class MCPServerInfo(BaseModel):
    name: str
    version: str
    description: str
    tools: List[Dict[str, Any]]
    authentication: Dict[str, Any]
