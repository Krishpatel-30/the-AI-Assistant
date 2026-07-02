from responses import responses
from datetime import datetime
from jokes import random_joke
from quotes import random_quote
from calculator import calculate

print("=" * 45)
print("🤖 KRISH AI ASSISTANT")
print("=" * 45)

name = input("Enter your name: ").title()

print(f"\nHello {name}! 👋")
print("Type 'help' to see available commands.\n")

while True:

    user = input(f"{name}: ").lower().strip()

    if user in ["bye", "exit"]:
        print("Bot: Goodbye! Have a wonderful day! 👋")
        break

    elif user == "time":
        print("Bot:", datetime.now().strftime("%I:%M %p"))

    elif user == "date":
        print("Bot:", datetime.now().strftime("%d-%m-%Y"))

    elif user == "day":
        print("Bot:", datetime.now().strftime("%A"))

    elif user == "joke":
        print("Bot:", random_joke())

    elif user == "quote":
        print("Bot:", random_quote())

    elif user.startswith("calculate"):
        expression = user.replace("calculate", "").strip()
        print("Bot:", calculate(expression))

    elif user.startswith("my name is"):
        name = user.replace("my name is", "").strip().title()
        print(f"Bot: Nice to meet you, {name}! 😊")

    elif user in responses:
        print("Bot:", responses[user])

    else:
        print("Bot: Sorry, I don't understand that command.")