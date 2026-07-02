import customtkinter as ctk
from components.bubble import ChatBubble


class ChatArea(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        title = ctk.CTkLabel(
            self,
            text="🤖 KRISH AI ASSISTANT",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=20)

        self.messages = ctk.CTkScrollableFrame(self)

        self.messages.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

    def add_bot_message(self, message):

        bubble = ChatBubble(
            self.messages,
            message,
            "bot"
        )

        bubble.pack(fill="x", padx=10, pady=5)

        self.messages._parent_canvas.yview_moveto(1.0)

        return bubble

    def add_user_message(self, message):

        bubble = ChatBubble(
            self.messages,
            message,
            "user"
        )

        bubble.pack(fill="x", padx=10, pady=5)

        self.messages._parent_canvas.yview_moveto(1.0)

        return bubble