import json
from typing import Any, Dict
from mcp.server.fastmcp import FastMCP
from schemas import (
    GenerateBioIn, GenerateBioOut, BioSuggestion,
    OpenerIn, OpenerOut, OpenerItem,
    ReplyIn, ReplyOut, ReplyOption,
    DatePlanIn, DatePlanOut, DatePlan,
    RedFlagIn, RedFlagOut, RedFlagItem,
    RoastIn, RoastOut,
    ValidateIn, ValidateOut,
    ScreenshotAnalysisIn, ScreenshotAnalysisOut, ExtractedProfileData,
    ConversationScreenshotIn, ConversationAnalysisOut
)
from llm import chat, analyze_image_with_text
from auth import check_bearer
from image_processor import image_processor

# Create MCP server
mcp = FastMCP(name="ai-wingman-mcp")

@mcp.tool()
async def validate_bearer(input: ValidateIn) -> ValidateOut:
    """Validate bearer token for Puch AI authentication"""
    ok = check_bearer(input.bearer_token)
    return ValidateOut(ok=ok, user_id=("puch_user" if ok else None))

@mcp.tool()
async def analyze_profile_screenshot(input: ScreenshotAnalysisIn) -> ScreenshotAnalysisOut:
    """Analyze dating profile screenshots and generate responses"""
    try:
        # Decode and process image
        image = image_processor.decode_base64_image(input.image_data)
        
        # Method 1: OCR text extraction
        extracted_text = image_processor.extract_text_from_image(image)
        
        # Method 2: AI vision analysis (as backup/enhancement)
        vision_prompt = f"""
Analyze this dating profile screenshot. Extract and identify:
1. Name and age
2. Bio/description text
3. Interests and hobbies mentioned
4. Education and work info
5. Location
6. Photo descriptions
7. Any red flags or concerning content

Context: {input.context}

Provide structured information that can help craft personalized conversation starters.
"""
        
        vision_analysis = await analyze_image_with_text(input.image_data, vision_prompt)
        
        # Extract structured profile data
        profile_data_dict = image_processor.extract_profile_data(extracted_text)
        profile_data = ExtractedProfileData(**profile_data_dict)
        
        # Enhance with vision analysis
        enhanced_text = f"OCR Text: {extracted_text}\n\nAI Vision Analysis: {vision_analysis}"
        
        # Generate conversation openers based on extracted data
        opener_prompt = f"""
Based on this dating profile analysis:
{enhanced_text}

Generate 5 personalized conversation openers that:
1. Reference something specific from their profile
2. Are engaging and show genuine interest
3. Avoid generic "hey" messages
4. Match a {input.context or 'witty'} tone
5. Include natural follow-up possibilities

For each opener, provide:
- The opener text
- 2 follow-up messages
- Why this opener works for this specific profile
"""
        
        opener_content = await chat([{"role": "user", "content": opener_prompt}], temperature=0.8)
        opener_data = _force_json(opener_content)
        
        openers = []
        for o in opener_data.get("openers", [])[:5]:
            openers.append(OpenerItem(
                text=o.get("text", ""),
                follow_ups=(o.get("follow_ups") or [])[:2],
                rationale=o.get("rationale", "")
            ))
        
        # Check for red flags
        red_flag_prompt = f"""
Analyze this dating profile for potential red flags or safety concerns:
{enhanced_text}

Look for:
- Controlling language
- Inappropriate requests
- Suspicious or inconsistent information
- Boundary-crossing content
- Potentially unsafe situations

Provide specific flags with severity levels and boundary statements.
"""
        
        red_flag_content = await chat([{"role": "user", "content": red_flag_prompt}], temperature=0.3)
        red_flag_data = _force_json(red_flag_content)
        
        red_flags = []
        for rf in red_flag_data.get("items", []):
            red_flags.append(RedFlagItem(
                flag=rf.get("flag", ""),
                severity=rf.get("severity", "low"),
                why=rf.get("why", ""),
                boundary_statement=rf.get("boundary_statement", "")
            ))
        
        # Generate analysis summary
        summary_prompt = f"""
Provide a brief, helpful summary of this dating profile analysis:
{enhanced_text}

Include:
- Key talking points
- Compatibility indicators
- Conversation strategy recommendations
- Overall impression
"""
        
        analysis_summary = await chat([{"role": "user", "content": summary_prompt}], temperature=0.6)
        
        return ScreenshotAnalysisOut(
            extracted_text=enhanced_text,
            profile_data=profile_data,
            suggested_openers=openers,
            red_flags=red_flags,
            analysis_summary=analysis_summary
        )
        
    except Exception as e:
        # Return error information
        return ScreenshotAnalysisOut(
            extracted_text=f"Error processing image: {str(e)}",
            profile_data=None,
            suggested_openers=[],
            red_flags=[],
            analysis_summary="Unable to analyze image. Please ensure image is clear and contains a dating profile."
        )

@mcp.tool()
async def analyze_conversation_screenshot(input: ConversationScreenshotIn) -> ConversationAnalysisOut:
    """Analyze conversation screenshots and suggest replies"""
    try:
        # Decode image
        image = image_processor.decode_base64_image(input.image_data)
        
        # Extract conversation text
        extracted_text = image_processor.extract_text_from_image(image)
        
        # AI vision analysis for conversation context
        vision_prompt = f"""
Analyze this conversation screenshot. Extract:
1. All messages in chronological order
2. Who sent each message (if distinguishable)
3. Timestamps if visible
4. Conversation context and mood
5. Last message that needs a response

My role in conversation: {input.my_role}
Additional context: {input.context}

Provide the conversation flow and identify what type of response would be most appropriate.
"""
        
        vision_analysis = await analyze_image_with_text(input.image_data, vision_prompt)
        
        # Parse messages (simplified - could be enhanced)
        messages = []
        lines = extracted_text.split('\n')
        for line in lines:
            if line.strip():
                messages.append({"text": line.strip(), "sender": "unknown"})
        
        # Generate reply suggestions
        last_message = messages[-1]["text"] if messages else extracted_text
        
        reply_prompt = f"""
Based on this conversation:
{vision_analysis}

Last message to respond to: "{last_message}"

Generate 3 thoughtful reply options:
1. Low-key/safe response
2. Medium engagement response  
3. Higher energy/flirty response (if appropriate)

Each reply should:
- Feel natural and conversational
- Match the conversation tone
- Move the conversation forward
- Include a boundary-safe alternative
- Have clear rationale for why it works

Context: {input.context}
"""
        
        reply_content = await chat([{"role": "user", "content": reply_prompt}], temperature=0.7)
        reply_data = _force_json(reply_content)
        
        replies = []
        for r in reply_data.get("options", [])[:3]:
            replies.append(ReplyOption(
                reply=r.get("reply", ""),
                vibe_level=r.get("vibe_level", "low"),
                boundary_safe_variant=r.get("boundary_safe_variant", ""),
                rationale=r.get("rationale", "")
            ))
        
        # Conversation analysis
        analysis_prompt = f"""
Analyze this conversation for:
1. Overall tone and mood
2. Interest level from both parties
3. Conversation momentum
4. Potential red flags or concerns
5. Relationship stage/progression

Conversation: {vision_analysis}
"""
        
        conversation_analysis = await chat([{"role": "user", "content": analysis_prompt}], temperature=0.5)
        
        # Next step advice
        next_step_prompt = f"""
Based on this conversation analysis, what should be the next strategic move?
Consider:
- Asking them out
- Continuing text conversation
- Sharing contact info
- Setting boundaries
- Moving to different topic

Conversation context: {vision_analysis}
"""
        
        next_step_advice = await chat([{"role": "user", "content": next_step_prompt}], temperature=0.6)
        
        return ConversationAnalysisOut(
            extracted_messages=messages,
            conversation_summary=vision_analysis,
            suggested_replies=replies,
            conversation_analysis=conversation_analysis,
            next_step_advice=next_step_advice
        )
        
    except Exception as e:
        return ConversationAnalysisOut(
            extracted_messages=[],
            conversation_summary=f"Error analyzing conversation: {str(e)}",
            suggested_replies=[],
            conversation_analysis="Unable to analyze conversation screenshot.",
            next_step_advice="Please try uploading a clearer image."
        )

@mcp.tool()
async def generate_bio(input: GenerateBioIn) -> GenerateBioOut:
    """Generate improved dating app bios based on user's current profile"""
    prompt = f"""
User's current bio/prompts/interests:
{input.profile_text}

Goal: Generate 3 improved bios for {input.app}.
Tone: {input.tone}. Length: {input.length}.

For each bio: provide keys: text, why_it_works, dos[3], donts[3].
Return strict JSON {{ "suggestions": [...] }}.
"""
    content = await chat([{"role": "user", "content": prompt}], temperature=0.6)
    data = _force_json(content)
    items = []
    for s in data.get("suggestions", [])[:3]:
        items.append(BioSuggestion(
            text=s.get("text", ""),
            why_it_works=s.get("why_it_works", ""),
            dos=(s.get("dos") or [])[:3],
            donts=(s.get("donts") or [])[:3]  # ✅ FIXED: Added closing bracket
        ))
    return GenerateBioOut(suggestions=items)

@mcp.tool()
async def opener(input: OpenerIn) -> OpenerOut:
    """Generate personalized conversation openers based on their profile"""
    prompt = f"""
Their profile:
{input.their_profile_text}

My profile (optional):
{input.my_profile}

Context (optional):
{input.context}

Generate {input.count} icebreakers in tone '{input.tone}'.
For each: keys 'text', 'follow_ups' (2), 'rationale'.
Return strict JSON {{ "openers": [...] }}.
"""
    content = await chat([{"role": "user", "content": prompt}], temperature=0.8)
    data = _force_json(content)
    items = []
    for o in data.get("openers", [])[:input.count]:
        items.append(OpenerItem(
            text=o.get("text", ""),
            follow_ups=(o.get("follow_ups") or [])[:2],
            rationale=o.get("rationale", "")
        ))
    return OpenerOut(openers=items)

@mcp.tool()
async def reply(input: ReplyIn) -> ReplyOut:
    """Generate thoughtful replies to continue conversations"""
    prompt = f"""
Partner message:
{input.partner_msg}

Thread context:
{input.thread_context}

Intent: {input.intent}
Tone: {input.tone}

Provide 3 replies with keys:
- reply
- vibe_level (low|medium|high)
- boundary_safe_variant
- rationale

Return strict JSON {{ "options": [...] }}.
"""
    content = await chat([{"role": "user", "content": prompt}], temperature=0.7)
    data = _force_json(content)
    opts = []
    for o in data.get("options", [])[:3]:
        opts.append(ReplyOption(
            reply=o.get("reply", ""),
            vibe_level=o.get("vibe_level", "low"),
            boundary_safe_variant=o.get("boundary_safe_variant", ""),
            rationale=o.get("rationale", "")
        ))
    return ReplyOut(options=opts)

@mcp.tool()
async def date_plan(input: DatePlanIn) -> DatePlanOut:
    """Create thoughtful first date plans based on interests and budget"""
    interests = ", ".join(input.interests)
    prompt = f"""
City: {input.city}
Budget: {input.budget}
Interests: {interests}
Vibe: {input.vibe}
Duration hours: {input.duration_hours}

Propose 3 first-date plans (escalating slightly).
Each plan fields:
- title
- steps (3-5)
- opener_line
- rain_plan (if outdoors)
- booking_tips (2-3)

Return strict JSON {{ "plans": [...] }}.
"""
    content = await chat([{"role": "user", "content": prompt}], temperature=0.6)
    data = _force_json(content)
    plans = []
    for p in data.get("plans", [])[:3]:
        plans.append(DatePlan(
            title=p.get("title", ""),
            steps=(p.get("steps") or [])[:5],
            opener_line=p.get("opener_line", ""),
            rain_plan=p.get("rain_plan"),
            booking_tips=(p.get("booking_tips") or [])[:3]  # ✅ FIXED: Added closing bracket
        ))
    return DatePlanOut(plans=plans)

@mcp.tool()
async def red_flag_check(input: RedFlagIn) -> RedFlagOut:
    """Analyze profiles for potential red flags and safety concerns"""
    prompt = f"""
Analyze profile for red flags. For each, include:
- flag
- severity (low|medium|high)
- why
- boundary_statement

Profile:
{input.profile_text}

Return strict JSON {{ "items": [...] }}.
"""
    content = await chat([{"role": "user", "content": prompt}], temperature=0.3)
    data = _force_json(content)
    items = []
    for i in data.get("items", []):
        items.append(RedFlagItem(
            flag=i.get("flag", ""),
            severity=i.get("severity", "low"),
            why=i.get("why", ""),
            boundary_statement=i.get("boundary_statement", "")
        ))
    return RedFlagOut(items=items)

@mcp.tool()
async def profile_roast(input: RoastIn) -> RoastOut:
    """Provide constructive feedback on dating profiles with humor"""
    prompt = f"""
Bio:
{input.bio}

Images (described):
{input.images_desc}

Provide:
- roast (light-hearted but helpful)
- reorder_advice[] (photo lineup tips)
- quick_fixes[] (3-5 actions)

Return strict JSON with keys: roast, reorder_advice, quick_fixes.
"""
    content = await chat([{"role": "user", "content": prompt}], temperature=0.5)
    data = _force_json(content)
    return RoastOut(
        roast=data.get("roast", ""),
        reorder_advice=(data.get("reorder_advice") or [])[:5],
        quick_fixes=(data.get("quick_fixes") or [])[:5]
    )

def _force_json(content: str) -> Dict[str, Any]:
    """Helper to parse JSON from AI response"""
    try:
        return json.loads(content)
    except Exception:
        try:
            # Try to extract JSON from response
            start = content.find("{")
            end = content.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(content[start:end])
        except Exception:
            pass
        # Return empty structure if parsing fails
        return {
            "suggestions": [], 
            "openers": [], 
            "options": [], 
            "plans": [], 
            "items": []
        }

def get_mcp_app():
    """Get the MCP app for mounting in FastAPI"""
    from fastapi import FastAPI
    
    # Create a FastAPI app that wraps the MCP tools
    mcp_app = FastAPI(title="MCP Tools")
    
    # Add a simple endpoint to verify MCP is working
    @mcp_app.get("/")
    async def mcp_root():
        return {
            "status": "MCP server running",
            "tools": [
                "generate_bio", "opener", "reply", 
                "date_plan", "red_flag_check", "profile_roast",
                "analyze_profile_screenshot", "analyze_conversation_screenshot"
            ]
        }
    
    # Add individual tool endpoints
    @mcp_app.post("/tools/generate_bio")
    async def bio_endpoint(input: GenerateBioIn):
        return await generate_bio(input)
    
    @mcp_app.post("/tools/opener")
    async def opener_endpoint(input: OpenerIn):
        return await opener(input)
        
    @mcp_app.post("/tools/reply")
    async def reply_endpoint(input: ReplyIn):
        return await reply(input)
        
    @mcp_app.post("/tools/date_plan")
    async def date_plan_endpoint(input: DatePlanIn):
        return await date_plan(input)
        
    @mcp_app.post("/tools/red_flag_check")
    async def red_flag_endpoint(input: RedFlagIn):
        return await red_flag_check(input)
        
    @mcp_app.post("/tools/profile_roast")
    async def roast_endpoint(input: RoastIn):
        return await profile_roast(input)
    
    # NEW: Screenshot analysis endpoints
    @mcp_app.post("/tools/analyze_profile_screenshot")
    async def profile_screenshot_endpoint(input: ScreenshotAnalysisIn):
        return await analyze_profile_screenshot(input)
    
    @mcp_app.post("/tools/analyze_conversation_screenshot")
    async def conversation_screenshot_endpoint(input: ConversationScreenshotIn):
        return await analyze_conversation_screenshot(input)
    
    return mcp_app
