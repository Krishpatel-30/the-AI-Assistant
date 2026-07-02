import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FILE = os.path.join(DATA_DIR, "history.json")


def load_history():

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(FILE):
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []


def save_message(sender, message):

    history = load_history()

    history.append({
        "sender": sender,
        "message": message
    })

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

    print("Saved:", sender, message)