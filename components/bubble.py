import customtkinter as ctk
from datetime import datetime


class ChatBubble(ctk.CTkFrame):

    def __init__(self, master, message, sender="bot"):
        super().__init__(master, fg_color="transparent")

        current_time = datetime.now().strftime("%H:%M")

        if sender == "bot":
            bubble_color = "#2B2B2B"
            text = f"🤖  {message}\n\n🕒 {current_time}"
            anchor = "w"
        else:
            bubble_color = "#2563EB"
            text = f"{message}\n\n🕒 {current_time} 👤"
            anchor = "e"

        bubble = ctk.CTkLabel(
            self,
            text=text,
            fg_color=bubble_color,
            text_color="white",
            corner_radius=22,
            wraplength=500,
            justify="left",
            padx=15,
            pady=12,
            font=("Segoe UI", 14)
        )

        bubble.pack(anchor=anchor, padx=15, pady=6)