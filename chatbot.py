from responses import responses
from jokes import random_joke
from quotes import random_quote
from calculator import calculate
from datetime import datetime

username = "User"

def get_response(user):

    global username

    user = user.lower().strip()

    if user in ["bye", "exit"]:
        return "Goodbye! 👋"

    elif user == "time":
        return datetime.now().strftime("%I:%M %p")

    elif user == "date":
        return datetime.now().strftime("%d-%m-%Y")

    elif user == "day":
        return datetime.now().strftime("%A")

    elif user in ["joke", "jokes"]:
        return random_joke()

    elif user in ["quote", "quotes"]:
        return random_quote()

    elif user == "calculator":
        return "Example: calculate 10+20"

    elif user.startswith("calculate"):
        expression = user.replace("calculate", "").strip()
        return calculate(expression)

    elif user.startswith("my name is"):
        username = user.replace("my name is", "").strip().title()
        return f"Nice to meet you {username}! 😊"

    elif user in responses:
        return responses[user]

    else:
        return "Sorry, I don't understand."