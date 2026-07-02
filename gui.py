import customtkinter as ctk
import threading
import time

from chatbot import get_response
from storage import create_chat, save_message
from components.sidebar import Sidebar
from components.chat_area import ChatArea
from components.input_bar import InputBar

# -----------------------------
# Appearance
# -----------------------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class KrishAIApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("🤖 Krish AI Assistant")
        self.geometry("1200x750")
        self.minsize(1100, 700)

        # Create first chat
        self.current_chat = create_chat()

        self.build_ui()

    # -----------------------------
    # Build UI
    # -----------------------------
    def build_ui(self):

        self.main = ctk.CTkFrame(self)
        self.main.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = Sidebar(
            self.main,
            self.new_chat
        )
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

    # -----------------------------
    # Send Message
    # -----------------------------
    def send_message(self, message):

        # Show user message
        self.chat.add_user_message(message)

        # Save user message
        save_message(
            self.current_chat,
            "user",
            message
        )

        # Show typing bubble
        typing = self.chat.add_bot_message("Typing...")

        def bot_reply():

            time.sleep(1)

            response = get_response(message)

            self.after(
                0,
                lambda: self.finish_reply(
                    typing,
                    response
                )
            )

        threading.Thread(
            target=bot_reply,
            daemon=True
        ).start()

    # -----------------------------
    # Finish Reply
    # -----------------------------
    def finish_reply(self, typing_bubble, response):

        typing_bubble.destroy()

        self.chat.add_bot_message(response)

        save_message(
            self.current_chat,
            "bot",
            response
        )

    # -----------------------------
    # New Chat
    # -----------------------------
    def new_chat(self):

        # Create new chat file
        self.current_chat = create_chat()

        # Clear chat window
        for widget in self.chat.messages.winfo_children():
            widget.destroy()

        # Show welcome message
        self.chat.add_bot_message(
            "👋 New chat started!\nHow can I help you today?"
        )