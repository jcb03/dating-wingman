from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# Existing schemas
class GenerateBioIn(BaseModel):
    profile_text: str = Field(..., description="User's interests, personality, background")
    tone: str = Field("confident", description="confident|playful|serious|witty")
    length: str = Field("medium", description="short|medium|long")
    app: str = Field("tinder", description="tinder|bumble|hinge|other")

class OpenerIn(BaseModel):
    their_profile_text: str = Field(..., description="Their profile information")
    tone: str = Field("friendly", description="friendly|playful|flirty|casual")
    count: int = Field(3, description="Number of openers to generate")

class ReplyIn(BaseModel):
    partner_msg: str = Field(..., description="What they said")
    intent: str = Field("continue", description="continue|flirt|ask_out|deflect")
    tone: str = Field("friendly", description="friendly|playful|witty|serious")

class DatePlanIn(BaseModel):
    city: str = Field(..., description="City/location for the date")
    budget: str = Field("medium", description="low|medium|high")
    interests: str = Field("", description="Shared interests or activities")
    vibe: str = Field("casual", description="casual|romantic|adventurous|cultural")

class RedFlagIn(BaseModel):
    profile_text: str = Field(..., description="Profile text or messages to analyze")

class RoastIn(BaseModel):
    bio: str = Field(..., description="Dating profile bio")
    images_desc: str = Field("", description="Description of profile images")

# Screenshot analysis schemas
class ScreenshotAnalysisIn(BaseModel):
    image_data: str = Field(..., description="Base64 encoded image data")
    analysis_type: str = Field("profile", description="profile|conversation|match")
    context: Optional[str] = Field("", description="Additional context")

class ConversationScreenshotIn(BaseModel):
    image_data: str = Field(..., description="Base64 encoded conversation screenshot")
    my_role: str = Field("sender", description="sender|receiver")
    context: Optional[str] = Field("", description="Additional context")

# New validate schema
class ValidateOut(BaseModel):
    phone_number: str = Field(..., description="Phone number in country_code+number format")

# Response schemas (optional but recommended)
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

class ScreenshotAnalysisOut(BaseModel):
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

class ConversationAnalysisOut(BaseModel):
    extracted_messages: List[Dict[str, Any]] = []
    conversation_summary: str
    suggested_replies: List[SuggestedReply]
    conversation_analysis: str
    next_step_advice: str
    my_role: str = "sender"
    context: str = ""
