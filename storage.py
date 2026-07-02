import os
import json
import uuid

DATA_FOLDER = "data/chats"

os.makedirs(DATA_FOLDER, exist_ok=True)


def create_chat():

    chat_id = str(uuid.uuid4())[:8]

    filename = os.path.join(
        DATA_FOLDER,
        f"{chat_id}.json"
    )

    with open(filename, "w") as file:
        json.dump([], file, indent=4)

    return chat_id


def save_message(chat_id, sender, message):

    filename = os.path.join(
        DATA_FOLDER,
        f"{chat_id}.json"
    )

    if os.path.exists(filename):

        with open(filename, "r") as file:
            history = json.load(file)

    else:
        history = []

    history.append(
        {
            "sender": sender,
            "message": message
        }
    )

    with open(filename, "w") as file:
        json.dump(history, file, indent=4)


def load_chat(chat_id):

    filename = os.path.join(
        DATA_FOLDER,
        f"{chat_id}.json"
    )

    if not os.path.exists(filename):
        return []

    with open(filename, "r") as file:
        return json.load(file)


def list_chats():

    chats = []

    for file in os.listdir(DATA_FOLDER):

        if file.endswith(".json"):
            chats.append(file.replace(".json", ""))

    return chats