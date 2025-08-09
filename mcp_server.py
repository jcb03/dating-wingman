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
    ValidateIn, ValidateOut
)
from llm import chat
from auth import check_bearer

# Create MCP server
mcp = FastMCP(name="ai-wingman-mcp")

@mcp.tool()
async def validate_bearer(input: ValidateIn) -> ValidateOut:
    """Validate bearer token for Puch AI authentication"""
    ok = check_bearer(input.bearer_token)
    return ValidateOut(ok=ok, user_id=("puch_user" if ok else None))

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
            donts=(s.get("donts") or [])[:3],
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
            booking_tips=(p.get("booking_tips") or [])[:3],
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
            boundary_statement=i.get("boundary_statement", ""),
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
        quick_fixes=(data.get("quick_fixes") or [])[:5],
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
    return mcp.run()
