import os
import json
import uuid
from datetime import datetime

DATA_FOLDER = "data/chats"

os.makedirs(DATA_FOLDER, exist_ok=True)


# --------------------------------------------------
# Time
# --------------------------------------------------

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# --------------------------------------------------
# Create Chat
# --------------------------------------------------

def create_chat():

    chat_id = str(uuid.uuid4())[:8]

    chat = {
        "title": "New Chat",
        "created_at": current_time(),
        "updated_at": current_time(),
        "messages": []
    }

    save_chat(chat_id, chat)

    return chat_id


# --------------------------------------------------
# Save Chat
# --------------------------------------------------

def save_chat(chat_id, chat):

    filename = os.path.join(
        DATA_FOLDER,
        f"{chat_id}.json"
    )

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            chat,
            file,
            indent=4,
            ensure_ascii=False
        )


# --------------------------------------------------
# Load Chat
# --------------------------------------------------

def load_chat(chat_id):

    filename = os.path.join(
        DATA_FOLDER,
        f"{chat_id}.json"
    )

    if not os.path.exists(filename):
        return None

    try:

        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception:

        return None


# --------------------------------------------------
# Save Message
# --------------------------------------------------

def save_message(chat_id, sender, message):

    chat = load_chat(chat_id)

    if chat is None:
        return

    chat["messages"].append({
        "sender": sender,
        "message": message
    })

    chat["updated_at"] = current_time()

    if (
        sender == "user"
        and chat["title"] == "New Chat"
    ):
        chat["title"] = message[:40]

    save_chat(chat_id, chat)


# --------------------------------------------------
# List Chats
# --------------------------------------------------

def list_chats():

    chats = []

    for filename in os.listdir(DATA_FOLDER):

        if not filename.endswith(".json"):
            continue

        chat_id = filename[:-5]

        chat = load_chat(chat_id)

        if chat is None:
            continue

        chats.append({
            "id": chat_id,
            "title": chat.get("title", "New Chat"),
            "created_at": chat.get("created_at", ""),
            "updated_at": chat.get("updated_at", ""),
            "message_count": len(chat.get("messages", []))
        })

    chats.sort(
        key=lambda x: x["updated_at"],
        reverse=True
    )

    return chats


# --------------------------------------------------
# Latest Chat
# --------------------------------------------------

def get_last_chat():

    chats = list_chats()

    if chats:
        return chats[0]["id"]

    return None


# --------------------------------------------------
# Rename Chat
# --------------------------------------------------

def rename_chat(chat_id, title):

    chat = load_chat(chat_id)

    if chat is None:
        return

    chat["title"] = title
    chat["updated_at"] = current_time()

    save_chat(chat_id, chat)


# --------------------------------------------------
# Delete Chat
# --------------------------------------------------

def delete_chat(chat_id):

    filename = os.path.join(
        DATA_FOLDER,
        f"{chat_id}.json"
    )

    if os.path.exists(filename):
        os.remove(filename)


# --------------------------------------------------
# Chat Exists
# --------------------------------------------------

def chat_exists(chat_id):

    filename = os.path.join(
        DATA_FOLDER,
        f"{chat_id}.json"
    )

    return os.path.exists(filename)