import os
import json
import uuid
from datetime import datetime

DATA_FOLDER = "data/chats"

os.makedirs(DATA_FOLDER, exist_ok=True)


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# -----------------------------
# Create Chat
# -----------------------------
def create_chat():

    chat_id = str(uuid.uuid4())[:8]

    filename = os.path.join(
        DATA_FOLDER,
        f"{chat_id}.json"
    )

    chat = {
        "title": "New Chat",
        "created_at": current_time(),
        "updated_at": current_time(),
        "messages": []
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(chat, file, indent=4)

    return chat_id


# -----------------------------
# Load Chat
# -----------------------------
def load_chat(chat_id):

    filename = os.path.join(
        DATA_FOLDER,
        f"{chat_id}.json"
    )

    if not os.path.exists(filename):
        return None

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


# -----------------------------
# Save Entire Chat
# -----------------------------
def save_chat(chat_id, chat):

    filename = os.path.join(
        DATA_FOLDER,
        f"{chat_id}.json"
    )

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(chat, file, indent=4)


# -----------------------------
# Save One Message
# -----------------------------
def save_message(chat_id, sender, message):

    chat = load_chat(chat_id)

    if chat is None:
        return

    chat["messages"].append({
        "sender": sender,
        "message": message
    })

    chat["updated_at"] = current_time()

    # Automatically rename first chat
    if chat["title"] == "New Chat" and sender == "user":
        chat["title"] = message[:30]

    save_chat(chat_id, chat)


# -----------------------------
# List Chats
# -----------------------------
def list_chats():

    chats = []

    for filename in os.listdir(DATA_FOLDER):

        if filename.endswith(".json"):

            chat_id = filename.replace(".json", "")

            chat = load_chat(chat_id)

            if chat:

                chats.append({
                    "id": chat_id,
                    "title": chat.get("title", "New Chat"),
                    "created_at": chat.get("created_at", ""),
                    "updated_at": chat.get("updated_at", "")
                })

    chats.sort(
        key=lambda x: x["updated_at"],
        reverse=True
    )

    return chats


# -----------------------------
# Rename Chat
# -----------------------------
def rename_chat(chat_id, new_title):

    chat = load_chat(chat_id)

    if chat is None:
        return

    chat["title"] = new_title
    chat["updated_at"] = current_time()

    save_chat(chat_id, chat)


# -----------------------------
# Delete Chat
# -----------------------------
def delete_chat(chat_id):

    filename = os.path.join(
        DATA_FOLDER,
        f"{chat_id}.json"
    )

    if os.path.exists(filename):
        os.remove(filename)


# -----------------------------
# Get Chat Info
# -----------------------------
def get_chat(chat_id):

    return load_chat(chat_id)