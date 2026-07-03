from ai import ask_gemini, stream_gemini
from storage import load_chat
from web_search import WebSearch

# ---------------------------------------------
# Web Search Engine
# ---------------------------------------------

search_engine = WebSearch()


# ---------------------------------------------
# Normal Response
# ---------------------------------------------

def get_response(
    chat_id,
    pdf_text=None,
    use_web=False,
    user_question=""
):

    chat = load_chat(chat_id)

    if chat is None:
        return "Chat not found."

    context = None

    # -----------------------------
    # PDF Context
    # -----------------------------

    if pdf_text:

        context = (
            "Answer using the following PDF context.\n\n"
            + pdf_text
        )

    # -----------------------------
    # Internet Context
    # -----------------------------

    elif use_web:

        results = search_engine.search(
            user_question
        )

        context = (
            "Answer using the following internet search results.\n\n"
            + search_engine.build_context(results)
        )

    # -----------------------------
    # Gemini
    # -----------------------------

    return ask_gemini(
        chat["messages"],
        context
    )


# ---------------------------------------------
# Streaming
# ---------------------------------------------

def stream_response(
    chat_id,
    pdf_text=None,
    use_web=False,
    user_question=""
):

    chat = load_chat(chat_id)

    if chat is None:
        yield "Chat not found."
        return

    context = None

    if pdf_text:

        context = (
            "Answer using the following PDF context.\n\n"
            + pdf_text
        )

    elif use_web:

        results = search_engine.search(
            user_question
        )

        context = (
            "Answer using the following internet search results.\n\n"
            + search_engine.build_context(results)
        )

    yield from stream_gemini(
        chat["messages"],
        context
    )