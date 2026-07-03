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
            icon = "🤖"
        else:
            bubble_color = "#2563EB"
            anchor = "e"
            icon = "👤"

        self.container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.container.pack(
            anchor=anchor,
            padx=15,
            pady=6
        )

        self.label = ctk.CTkLabel(
            self.container,
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

        self.label.pack(fill="x")

        # Bottom row
        bottom = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )

        bottom.pack(
            fill="x",
            pady=(5, 0)
        )

        self.time_label = ctk.CTkLabel(
            bottom,
            text=f"{icon}  {self.current_time}",
            font=("Segoe UI", 11),
            text_color="gray"
        )

        self.time_label.pack(
            side="left"
        )

        # Copy button only for AI
        if sender == "bot":

            self.copy_btn = ctk.CTkButton(
                bottom,
                text="📋 Copy",
                width=70,
                height=24,
                font=("Segoe UI", 11),
                command=self.copy_message
            )

            self.copy_btn.pack(
                side="right"
            )

        self.set_text(message)

    # ---------------------------------------
    # Update Bubble
    # ---------------------------------------

    def set_text(self, message):

        self.message = message

        self.label.configure(
            text=message
        )

    # ---------------------------------------
    # Get Text
    # ---------------------------------------

    def get_text(self):

        return self.message

    # ---------------------------------------
    # Copy
    # ---------------------------------------

    def copy_message(self):

        self.clipboard_clear()
        self.clipboard_append(self.message)

        if self.sender == "bot":

            self.copy_btn.configure(
                text="✅ Copied"
            )

            self.after(
                1500,
                lambda: self.copy_btn.configure(
                    text="📋 Copy"
                )
            )