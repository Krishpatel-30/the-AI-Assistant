import customtkinter as ctk
from datetime import datetime
from components.markdown_renderer import MarkdownRenderer
from components.code_block import CodeBlock


class ChatBubble(ctk.CTkFrame):

    def __init__(self, master, message, sender="bot"):
        super().__init__(master, fg_color="transparent")

        self.sender = sender
        self.message = message
        self.markdown = MarkdownRenderer()
        self.current_time = datetime.now().strftime("%H:%M")

        # ---------------------------------
        # Colors
        # ---------------------------------

        if sender == "bot":

            self.bubble_color = "#2B2B2B"
            self.anchor = "w"
            self.icon = "🤖"

        else:

            self.bubble_color = "#2563EB"
            self.anchor = "e"
            self.icon = "👤"

        # ---------------------------------
        # Main Container
        # ---------------------------------

        self.container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.container.pack(
            anchor=self.anchor,
            padx=15,
            pady=6
        )

        # This frame will hold
        # labels + code blocks

        self.content = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )

        self.content.pack(fill="x")

        # ---------------------------------
        # Bottom Bar
        # ---------------------------------

        self.bottom = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )

        self.bottom.pack(
            fill="x",
            pady=(5, 0)
        )

        # Time

        self.time_label = ctk.CTkLabel(
            self.bottom,
            text=f"{self.icon}  {self.current_time}",
            font=("Segoe UI", 11),
            text_color="gray"
        )

        self.time_label.pack(
            side="left"
        )

        # Copy button only for AI

        if sender == "bot":

            self.copy_btn = ctk.CTkButton(
                self.bottom,
                text="📋 Copy",
                width=80,
                height=26,
                font=("Segoe UI", 11),
                command=self.copy_message
            )

            self.copy_btn.pack(
                side="right"
            )

        # Render message

        self.set_text(message)
        message = self.markdown.render(message)
            # =====================================================
    # Render Message
    # =====================================================

    def set_text(self, message):

        self.message = message

        # Clear previous content
        for widget in self.content.winfo_children():
            widget.destroy()

        # Split message into normal text and code blocks
        parts = message.split("```")

        for index, part in enumerate(parts):

            # -----------------------------
            # Normal Text
            # -----------------------------
            if index % 2 == 0:

                if part.strip():

                    label = ctk.CTkLabel(
                        self.content,
                        text=part.strip(),
                        fg_color=self.bubble_color,
                        text_color="white",
                        corner_radius=20,
                        justify="left",
                        wraplength=650,
                        padx=15,
                        pady=12,
                        font=("Segoe UI", 14)
                    )

                    label.pack(
                        fill="x",
                        pady=(0, 8)
                    )

            # -----------------------------
            # Code Block
            # -----------------------------
            else:

                code = part.strip()

                language = "Code"

                lines = code.splitlines()

                if len(lines) > 1:

                    language = lines[0].strip()

                    code = "\n".join(lines[1:])

                code_widget = CodeBlock(
                    self.content,
                    code,
                    language
                )

                code_widget.pack(
                    fill="x",
                    pady=(0, 8)
                )

    # =====================================================
    # Return Message
    # =====================================================

    def get_text(self):

        return self.message

    # =====================================================
    # Copy Message
    # =====================================================

    def copy_message(self):

        self.clipboard_clear()
        self.clipboard_append(self.message)

        if hasattr(self, "copy_btn"):

            self.copy_btn.configure(
                text="✅ Copied"
            )

            self.after(
                1500,
                lambda: self.copy_btn.configure(
                    text="📋 Copy"
                )
            )