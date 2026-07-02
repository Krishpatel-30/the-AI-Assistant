import os
import json
import uuid
from datetime import datetime

DATA_FOLDER = "data/chats"

os.makedirs(DATA_FOLDER, exist_ok=True)


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


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


def load_chat(chat_id):

    filename = os.path.join(
        DATA_FOLDER,
        f"{chat_id}.json"
    )

    if not os.path.exists(filename):
        return None

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def save_chat(chat_id, chat):

    filename = os.path.join(
        DATA_FOLDER,
        f"{chat_id}.json"
    )

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(chat, file, indent=4)


def save_message(chat_id, sender, message):

    chat = load_chat(chat_id)

    if chat is None:
        return

    chat["messages"].append(
        {
            "sender": sender,
            "message": message
        }
    )

    chat["updated_at"] = current_time()

    # First user message becomes title
    if chat["title"] == "New Chat" and sender == "user":
        chat["title"] = message[:30]

    save_chat(chat_id, chat)


def list_chats():

    chats = []

    for file in os.listdir(DATA_FOLDER):

        if file.endswith(".json"):

            chat_id = file.replace(".json", "")

            chat = load_chat(chat_id)

            if chat:

                chats.append(
                    {
                        "id": chat_id,
                        "title": chat["title"],
                        "updated_at": chat["updated_at"]
                    }
                )

    chats.sort(
        key=lambda x: x["updated_at"],
        reverse=True
    )

    return chats


def rename_chat(chat_id, new_title):

    chat = load_chat(chat_id)

    if chat is None:
        return

    chat["title"] = new_title
    chat["updated_at"] = current_time()

    save_chat(chat_id, chat)


def delete_chat(chat_id):

    filename = os.path.join(
        DATA_FOLDER,
        f"{chat_id}.json"
    )

    if os.path.exists(filename):
        os.remove(filename)