import customtkinter as ctk
from datetime import datetime


class ChatBubble(ctk.CTkFrame):

    def __init__(self, master, message, sender="bot"):
        super().__init__(master, fg_color="transparent")

        self.sender = sender
        self.message = message
        self.current_time = datetime.now().strftime("%H:%M")

        if sender == "bot":
            bubble_color = "#2B2B2B"
            anchor = "w"
            self.prefix = "🤖  "
            self.suffix = f"\n\n🕒 {self.current_time}"

        else:
            bubble_color = "#2563EB"
            anchor = "e"
            self.prefix = ""
            self.suffix = f"\n\n🕒 {self.current_time} 👤"

        self.label = ctk.CTkLabel(
            self,
            text="",
            fg_color=bubble_color,
            text_color="white",
            corner_radius=22,
            wraplength=650,
            justify="left",
            padx=15,
            pady=12,
            font=("Segoe UI", 14)
        )

        self.label.pack(
            anchor=anchor,
            padx=15,
            pady=6
        )

        self.set_text(message)

    # -------------------------------------------------
    # Update Bubble Text
    # -------------------------------------------------

    def set_text(self, message):

        self.message = message

        self.label.configure(
            text=f"{self.prefix}{message}{self.suffix}"
        )

    # -------------------------------------------------
    # Get Current Message
    # -------------------------------------------------

    def get_text(self):

        return self.message