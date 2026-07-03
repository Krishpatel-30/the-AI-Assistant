from ai import ask_gemini, stream_gemini
from storage import load_chat


def get_response(chat_id):

    chat = load_chat(chat_id)

    if chat is None:
        return "Chat not found."

    return ask_gemini(
        chat["messages"]
    )


def stream_response(chat_id):

    chat = load_chat(chat_id)

    if chat is None:
        yield "Chat not found."
        return

    yield from stream_gemini(
        chat["messages"]
    )