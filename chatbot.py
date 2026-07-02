from responses import responses
from datetime import datetime
from jokes import random_joke
from quotes import random_quote
from calculator import calculate

user_name = "User"

def get_response(user):

    global user_name

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

    elif user.startswith("calculate"):
        expression = user.replace("calculate", "").strip()
        return calculate(expression)

    elif user == "calculator":
        return "Type: calculate 10+20"

    elif user.startswith("my name is"):
        user_name = user.replace("my name is", "").strip().title()
        return f"Nice to meet you {user_name}! 😊"

    elif user in responses:
        return responses[user]

    else:
        return "Sorry, I don't understand that."