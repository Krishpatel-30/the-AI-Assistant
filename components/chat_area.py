import customtkinter as ctk
from components.bubble import ChatBubble


class ChatArea(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        # ----------------------------------------
        # Title
        # ----------------------------------------

        self.title = ctk.CTkLabel(
            self,
            text="🤖 KRISH AI ASSISTANT",
            font=("Segoe UI", 28, "bold")
        )

        self.title.pack(
            pady=(20, 10)
        )

        # ----------------------------------------
        # Messages
        # ----------------------------------------

        self.messages = ctk.CTkScrollableFrame(
            self,
            corner_radius=12
        )

        self.messages.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

    # ----------------------------------------
    # Auto Scroll
    # ----------------------------------------

    def scroll_bottom(self):

        self.update_idletasks()

        try:
            self.messages._parent_canvas.yview_moveto(1.0)
        except Exception:
            pass

    # ----------------------------------------
    # Bot Message
    # ----------------------------------------

    def add_bot_message(self, message):

        bubble = ChatBubble(
            self.messages,
            message,
            "bot"
        )

        bubble.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.scroll_bottom()

        return bubble

    # ----------------------------------------
    # User Message
    # ----------------------------------------

    def add_user_message(self, message):

        bubble = ChatBubble(
            self.messages,
            message,
            "user"
        )

        bubble.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.scroll_bottom()

        return bubble

    # ----------------------------------------
    # Update Existing Bubble
    # (Needed for Streaming)
    # ----------------------------------------

    def update_message(self, bubble, text):

        bubble.set_text(text)

        self.scroll_bottom()

    # ----------------------------------------
    # Clear Messages
    # ----------------------------------------

    def clear_messages(self):

        for widget in self.messages.winfo_children():
            widget.destroy()

    # ----------------------------------------
    # Load Chat
    # ----------------------------------------

    def load_messages(self, messages):

        self.clear_messages()

        for msg in messages:

            if msg["sender"] == "user":

                self.add_user_message(
                    msg["message"]
                )

            else:

                self.add_bot_message(
                    msg["message"]
                )

        self.scroll_bottom()