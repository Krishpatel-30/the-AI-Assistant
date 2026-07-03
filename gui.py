import customtkinter as ctk
import threading
import queue
import os

from pdf_chat import PDFChat

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

        # ----------------------------------------
        # App State
        # ----------------------------------------

        self.stream_queue = queue.Queue()

        self.pdf = PDFChat()

        self.current_chat = get_last_chat()

        if self.current_chat is None:
            self.current_chat = create_chat()

        self.build_ui()

    # ==========================================================
    # BUILD UI
    # ==========================================================

    def build_ui(self):

        self.main = ctk.CTkFrame(self)
        self.main.pack(
            fill="both",
            expand=True
        )

        # ---------------- Sidebar ----------------

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

        # ---------------- Chat Area ----------------

        self.chat = ChatArea(
            self.main
        )

        self.chat.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ---------------- Input ----------------

        self.input = InputBar(
            self.chat,
            self.send_message,
            self.load_pdf
        )

        self.refresh_sidebar()

        self.load_chat(
            self.current_chat
        )

    # ==========================================================
    # REFRESH SIDEBAR
    # ==========================================================

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

    # ==========================================================
    # LOAD CHAT
    # ==========================================================

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
                "👋 Welcome to Krish AI Assistant!\n\n"
                "How can I help you today?"
            )

        self.refresh_sidebar()

    # ==========================================================
    # LOAD PDF
    # ==========================================================

    def load_pdf(self, file_path):

        try:

            pages = self.pdf.load_pdf(
                file_path
            )

            filename = os.path.basename(
                file_path
            )

            self.chat.add_bot_message(

                f"📄 PDF Loaded Successfully!\n\n"

                f"File : {filename}\n"

                f"Pages : {pages}\n\n"

                "You can now ask questions about this PDF."

            )

        except Exception as e:

            self.chat.add_bot_message(

                f"❌ Failed to load PDF.\n\n{e}"

            )

                # ==========================================================
    # SEND MESSAGE
    # ==========================================================

    def send_message(self, message):

        self.input.disable()

        # Show user message
        self.chat.add_user_message(message)

        save_message(
            self.current_chat,
            "user",
            message
        )

        self.refresh_sidebar()

        # Empty bot bubble for streaming
        self.current_bubble = self.chat.add_bot_message("")

        threading.Thread(
            target=self.stream_reply,
            args=(message,),
            daemon=True
        ).start()


    # ==========================================================
    # STREAM REPLY
    # ==========================================================

    def stream_reply(self, message):

        full_response = ""

        try:

            # ---------------- PDF ----------------

            if self.pdf.is_loaded():

                context = self.pdf.get_context(
                    message
                )

                generator = stream_response(
                    self.current_chat,
                    pdf_text=context
                )

            # ---------------- Web ----------------

            elif self.input.is_web_enabled():

                generator = stream_response(
                    self.current_chat,
                    use_web=True,
                    user_question=message
                )

            # ---------------- Normal ----------------

            else:

                generator = stream_response(
                    self.current_chat
                )

            # ---------------- Stream ----------------

            for chunk in generator:

                full_response += chunk

                self.after(
                    0,
                    lambda text=full_response:
                    self.current_bubble.set_text(text)
                )

            self.after(
                0,
                lambda:
                self.finish_reply(full_response)
            )

        except Exception as e:

            self.after(
                0,
                lambda:
                self.finish_reply(
                    f"❌ {e}"
                )
            )


    # ==========================================================
    # FINISH REPLY
    # ==========================================================

    def finish_reply(self, response):

        save_message(
            self.current_chat,
            "bot",
            response
        )

        self.refresh_sidebar()

        self.input.enable()

            # ==========================================================
    # NEW CHAT
    # ==========================================================

    def new_chat(self):

        self.current_chat = create_chat()

        self.chat.clear_messages()

        self.chat.add_bot_message(

            "👋 New chat started!\n\n"

            "How can I help you today?"

        )

        self.refresh_sidebar()

    # ==========================================================
    # RENAME CHAT
    # ==========================================================

    def rename_chat_dialog(self, chat_id):

        dialog = ctk.CTkInputDialog(

            title="Rename Chat",

            text="Enter a new title"

        )

        title = dialog.get_input()

        if title:

            title = title.strip()

            if title:

                rename_chat(

                    chat_id,

                    title

                )

                self.refresh_sidebar()

    # ==========================================================
    # DELETE CHAT
    # ==========================================================

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

    # ==========================================================
    # CLEAR CURRENT CHAT
    # ==========================================================

    def clear_current_chat(self):

        self.chat.clear_messages()

        self.chat.add_bot_message(

            "🗑 Chat cleared."

        )

    # ==========================================================
    # EXPORT CHAT
    # ==========================================================

    def export_chat(self):

        chat = load_chat(

            self.current_chat

        )

        if chat is None:

            return

        filename = f"{self.current_chat}.txt"

        with open(

            filename,

            "w",

            encoding="utf-8"

        ) as file:

            for msg in chat["messages"]:

                sender = msg["sender"].capitalize()

                file.write(

                    f"{sender}: "

                    f"{msg['message']}\n\n"

                )

        self.chat.add_bot_message(

            f"✅ Chat exported as\n{filename}"

        )

    # ==========================================================
    # COPY LAST RESPONSE
    # ==========================================================

    def copy_last_response(self):

        chat = load_chat(

            self.current_chat

        )

        if chat is None:

            return

        messages = chat["messages"]

        for msg in reversed(messages):

            if msg["sender"] == "bot":

                self.clipboard_clear()

                self.clipboard_append(

                    msg["message"]

                )

                break

    # ==========================================================
    # STOP STREAM
    # ==========================================================

    def stop_stream(self):

        self.stream_queue.put(

            "__STOP__"

        )