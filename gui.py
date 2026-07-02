import customtkinter as ctk
import threading
import time

from chatbot import get_response
from storage import (
    create_chat,
    save_message,
    list_chats,
    load_chat
)

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

        self.current_chat = create_chat()

        self.build_ui()

    # -----------------------------
    # Build UI
    # -----------------------------

    def build_ui(self):

        self.main = ctk.CTkFrame(self)
        self.main.pack(fill="both", expand=True)

        self.sidebar = Sidebar(
            self.main,
            self.new_chat
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.chat = ChatArea(self.main)

        self.chat.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.chat.add_bot_message(
            "👋 Welcome to Krish AI Assistant!\nHow can I help you today?"
        )

        self.input = InputBar(
            self.chat,
            self.send_message
        )

        self.refresh_sidebar()

    # -----------------------------
    # Sidebar
    # -----------------------------

    def refresh_sidebar(self):

        self.sidebar.clear_chat_list()

        chats = list_chats()

        for chat in chats:

            self.sidebar.add_chat_button(
                chat["id"],
                chat["title"],
                lambda cid=chat["id"]: self.load_chat(cid)
            )

        self.sidebar.highlight_chat(
            self.current_chat
        )

    # -----------------------------
    # Load Chat
    # -----------------------------

    def load_chat(self, chat_id):

        chat = load_chat(chat_id)

        if chat is None:
            return

        self.current_chat = chat_id

        self.chat.load_messages(
            chat["messages"]
        )

        self.refresh_sidebar()

    # -----------------------------
    # Send Message
    # -----------------------------

    def send_message(self, message):

        self.chat.add_user_message(message)

        save_message(
            self.current_chat,
            "user",
            message
        )

        typing = self.chat.add_bot_message(
            "Typing..."
        )

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

    def finish_reply(
        self,
        typing_bubble,
        response
    ):

        typing_bubble.destroy()

        self.chat.add_bot_message(response)

        save_message(
            self.current_chat,
            "bot",
            response
        )

        self.refresh_sidebar()

    # -----------------------------
    # New Chat
    # -----------------------------

    def new_chat(self):

        self.current_chat = create_chat()

        self.chat.clear_messages()

        self.chat.add_bot_message(
            "👋 New chat started!\nHow can I help you today?"
        )

        self.refresh_sidebar()