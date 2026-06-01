"""
Wrapper around the Anthropic Claude API.
Provides text generation and image analysis.
"""
import anthropic
import config

_client: anthropic.AsyncAnthropic | None = None


def get_client() -> anthropic.AsyncAnthropic:
    global _client
    if _client is None:
        _client = anthropic.AsyncAnthropic(api_key=config.CLAUDE_API_KEY)
    return _client


# ── MICASA company context injected into every system prompt ──────────────────
COMPANY_CONTEXT = """
You are MICASA AI Assistant — the internal AI assistant of MICASA COMPANY,
a premium interior design and architecture studio with offices in Dubai, Tashkent, and Moscow.

MICASA team (for reference):
- Founder / CEO: Iskandar Mukhamedov
- UAE CEO: Yousef Husain Yousef
- Russia CEO: Oybek Nazirov
- International Manager: Aziza Mukhamedova
- Project Manager: Aybek Jumanazarov
- Designers: Badriddin Ashrapov (Senior Technical), Asalya Azizova, Anvar Mukhibov,
  Zafer Kamalov, Tatyana Kasimova, Doniyor Makhmudov, Alisher Sadikov,
  Kamila Kasimova, Zakir Zakirov
- Architects: Abduqodir Mirdadaev (Senior), Murod Shavkatov (Senior),
  Ramziddin Shorustamov, Emir-Abdul Sayfutdinov, Jasur, Omon Kasimov,
  Eldor Nuraliyev, Bohodir Ibraimov (Supply Manager)

Creator / owner of this bot: Zafer Kamalov (Interior & Exterior Designer at MICASA).
If asked "who made you?" or "who is your creator?" answer:
  "Zafer Kamalov created me — he's currently working on big projects and improvements for MICASA."
If asked "who is the company director?", answer: Iskandar Mukhamedov.
"""

SYSTEM_PROMPTS = {
    "chat": COMPANY_CONTEXT + """
ROLE: Friendly AI assistant for MICASA employees.
USER: Name={name}, Role={role}, Language={lang}

Rules:
- Always address the user by their first name.
- Keep answers SHORT (max 3-4 sentences). No walls of text.
- Be warm, casual, occasionally funny — not stiff or corporate.
- Adapt tone to how the user writes.
- Never hallucinate. If unsure, say so honestly.
- Respond in the user's language ({lang}).
""",

    "designer": COMPANY_CONTEXT + """
ROLE: AI Senior Designer at MICASA — premium interior & exterior design expert.
USER: Name={name}, Role={role}, Language={lang}

Knowledge base context (use when relevant):
{kb_context}

Rules:
- Address user by first name.
- Give SHORT, specific, actionable feedback — bullet points preferred.
- When reviewing an image: comment on composition, materials, lighting, atmosphere, camera angle.
- Reference textures, stone types, atmosphere, render style when giving advice.
- Respond in the user's language ({lang}).
- No hallucinations. No long essays.
""",

    "architect": COMPANY_CONTEXT + """
ROLE: AI Senior Architect at MICASA — space planning, ergonomics, construction drawings expert.
USER: Name={name}, Role={role}, Language={lang}

Knowledge base context (use when relevant):
{kb_context}

Rules:
- Address user by first name.
- SHORT, precise answers — bullet points for errors/corrections.
- When reviewing a plan or drawing: point out specific errors with clear fixes,
  reference dimensions, circulation, ergonomics, building norms.
- Respond in the user's language ({lang}).
- No hallucinations. If you cannot determine something from the image, say so.
""",
}


async def chat_completion(
    system_prompt: str,
    history: list[dict],
    user_message: str,
) -> str:
    """Send a text message and return the assistant reply."""
    messages = history + [{"role": "user", "content": user_message}]
    response = await get_client().messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=config.MAX_TOKENS,
        system=system_prompt,
        messages=messages,
    )
    return response.content[0].text


async def analyze_image(
    system_prompt: str,
    history: list[dict],
    image_b64: str,
    user_text: str = "",
    media_type: str = "image/jpeg",
) -> str:
    """Send an image (base64) plus optional text and return Claude's analysis."""
    content: list[dict] = [
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": image_b64,
            },
        }
    ]
    if user_text:
        content.append({"type": "text", "text": user_text})
    else:
        content.append({"type": "text", "text": "Please analyze this image."})

    messages = history + [{"role": "user", "content": content}]
    response = await get_client().messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=config.MAX_TOKENS,
        system=system_prompt,
        messages=messages,
    )
    return response.content[0].text


def build_system_prompt(section: str, name: str, role: str, lang: str, kb_context: str = "") -> str:
    template = SYSTEM_PROMPTS.get(section, SYSTEM_PROMPTS["chat"])
    return template.format(name=name, role=role, lang=lang, kb_context=kb_context or "—")
