import customtkinter as ctk
import threading
from pdf_chat import PDFChat
import os
import queue

from chatbot import (
    get_response,
    stream_response
)
from storage import (
    create_chat,
    save_message,
    list_chats,
    load_chat,
    get_last_chat,
    rename_chat,
    delete_chat
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

        self.current_chat = get_last_chat()

        if self.current_chat is None:
            self.current_chat = create_chat()

        self.stream_queue = queue.Queue()
        self.pdf = PDFChat()

        self.build_ui()

    # -------------------------------------------------
    # Build UI
    # -------------------------------------------------

    def build_ui(self):

        self.main = ctk.CTkFrame(self)
        self.main.pack(fill="both", expand=True)

        self.sidebar = Sidebar(
            self.main,
            self.new_chat,
            self.rename_chat_dialog,
            self.delete_chat_dialog
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

        self.input = InputBar(
        self.chat,
            self.send_message,
            self.load_pdf
        )
        
        self.refresh_sidebar()

        self.load_chat(self.current_chat)

    # -------------------------------------------------
    # Sidebar
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Load Chat
    # -------------------------------------------------

    def load_chat(self, chat_id):

        chat = load_chat(chat_id)

        if chat is None:
            return

        self.current_chat = chat_id

        self.chat.load_messages(
            chat["messages"]
        )

        if len(chat["messages"]) == 0:

            self.chat.add_bot_message(
                "👋 Welcome to Krish AI Assistant!\nHow can I help you today?"
            )

        self.refresh_sidebar()

            # -------------------------------------------------
    # Load PDF
    # -------------------------------------------------

    def load_pdf(self, file_path):

        try:

            pages = self.pdf.load_pdf(file_path)

            filename = os.path.basename(file_path)

            self.chat.add_bot_message(
                f"📄 PDF Loaded Successfully!\n\n"
                f"File: {filename}\n"
                f"Pages: {pages}\n\n"
                "You can now ask questions about this PDF."
            )

        except Exception as e:

            self.chat.add_bot_message(
                f"❌ Failed to load PDF.\n\n{e}"
            )
    # -------------------------------------------------
    # Send Message
    # -------------------------------------------------

    def send_message(self, message):

        self.input.disable()

        self.chat.add_user_message(message)

        save_message(
            self.current_chat,
            "user",
            message
        )

        self.refresh_sidebar()

        typing = self.chat.add_bot_message(
            "Thinking..."
        )

    def bot_reply():

           


        # -----------------------------
        # PDF Mode (Highest Priority)
        # -----------------------------
        if self.pdf.is_loaded():

            context = self.pdf.get_context(message)

            response = get_response(
                self.current_chat,
                pdf_text=context
            )

        # -----------------------------
        # Web Search Mode
        # -----------------------------
        elif self.input.is_web_enabled():

            response = get_response(
            self.current_chat,
            use_web=True,
            user_question=message
            )

        # -----------------------------
        # Normal Chat
        # -----------------------------
        else:

            response = get_response(
            self.current_chat
            )

            self.after(
            0,
            lambda: self.finish_reply(
                typing,
                response
            )
        )
        # -------------------------------------------------
        # Finish Reply
        # -------------------------------------------------

        def finish_reply(
            self,
            typing_bubble,
            response
        ):

            typing_bubble.destroy()

            self.chat.add_bot_message(
                response
            )

            save_message(
                self.current_chat,
                "bot",
                response
            )

            self.refresh_sidebar()

            self.input.enable()

    # -------------------------------------------------
    # New Chat
    # -------------------------------------------------

    def new_chat(self):

        self.current_chat = create_chat()

        self.chat.clear_messages()

        self.chat.add_bot_message(
            "👋 New chat started!\nHow can I help you today?"
        )

        self.refresh_sidebar()

    # -------------------------------------------------
    # Rename Chat
    # -------------------------------------------------

    def rename_chat_dialog(self, chat_id):

        dialog = ctk.CTkInputDialog(
            title="Rename Chat",
            text="Enter new chat title:"
        )

        title = dialog.get_input()

        if title and title.strip():

            rename_chat(
                chat_id,
                title.strip()
            )

            self.refresh_sidebar()

    # -------------------------------------------------
    # Delete Chat
    # -------------------------------------------------

    def delete_chat_dialog(self, chat_id):

        delete_chat(chat_id)

        chats = list_chats()

        if chats:

            self.current_chat = chats[0]["id"]

        else:

            self.current_chat = create_chat()

        self.load_chat(
            self.current_chat
        )

        self.refresh_sidebar()