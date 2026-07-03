import os

from dotenv import load_dotenv
from google import genai

# --------------------------------------------------
# Load Environment
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=API_KEY)

# --------------------------------------------------
# System Prompt
# --------------------------------------------------

SYSTEM_PROMPT = """
You are Krish AI Assistant.

Rules:
- Be friendly and professional.
- Give detailed and accurate answers.
- Explain clearly.
- Format code inside Markdown code blocks.
- Use bullet points where appropriate.
- If you don't know something, say so instead of making it up.
"""

# --------------------------------------------------
# Build Conversation
# --------------------------------------------------

def build_conversation(history):

    conversation = SYSTEM_PROMPT + "\n\n"

    for msg in history:

        if msg["sender"] == "user":
            conversation += f"User: {msg['message']}\n"

        else:
            conversation += f"Assistant: {msg['message']}\n"

    return conversation


# --------------------------------------------------
# Normal Response
# --------------------------------------------------

def ask_gemini(history):

    conversation = build_conversation(history)

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conversation
        )

        return response.text

    except Exception as e:

        return f"❌ Gemini Error:\n\n{e}"


# --------------------------------------------------
# Streaming Response
# --------------------------------------------------

def stream_gemini(history):

    conversation = build_conversation(history)

    try:

        stream = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=conversation
        )

        for chunk in stream:

            if chunk.text:
                yield chunk.text

    except Exception as e:

        yield f"❌ Gemini Error:\n\n{e}"