import customtkinter as ctk
import threading
import time

from chatbot import get_response
from components.sidebar import Sidebar
from components.chat_area import ChatArea
from components.input_bar import InputBar

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class KrishAIApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("🤖 Krish AI Assistant")
        self.geometry("1200x750")
        self.minsize(1100, 700)

        self.build_ui()

    def build_ui(self):

        self.main = ctk.CTkFrame(self)
        self.main.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = Sidebar(self.main)
        self.sidebar.pack(side="left", fill="y")

        # Chat Area
        self.chat = ChatArea(self.main)
        self.chat.pack(side="right", fill="both", expand=True)

        # Welcome Message
        self.chat.add_bot_message(
            "👋 Welcome to Krish AI Assistant!\nHow can I help you today?"
        )

        # Input Bar
        self.input = InputBar(
            self.chat,
            self.send_message
        )

    def send_message(self, message):

        self.chat.add_user_message(message)

        typing = self.chat.add_bot_message("Typing...")

        def bot_reply():

            time.sleep(1)

            response = get_response(message)

            self.after(
                0,
                lambda: self.finish_reply(typing, response)
            )

        threading.Thread(
            target=bot_reply,
            daemon=True
        ).start()

    def finish_reply(self, typing_bubble, response):

        typing_bubble.destroy()

        self.chat.add_bot_message(response)