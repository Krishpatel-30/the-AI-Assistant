import customtkinter as ctk


class InputBar(ctk.CTkFrame):

    def __init__(self, master, send_callback):
        super().__init__(master)

        self.pack(fill="x", padx=20, pady=15)

        self.send_callback = send_callback

        # -----------------------------
        # Message Entry
        # -----------------------------
        self.entry = ctk.CTkTextbox(
            self,
            height=60,
            font=("Segoe UI", 15)
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(10, 5),
            pady=10
        )

        self.entry.bind("<Return>", self.on_enter)

        # -----------------------------
        # Buttons
        # -----------------------------
        self.emoji_btn = ctk.CTkButton(
            self,
            text="😊",
            width=45
        )
        self.emoji_btn.pack(side="left", padx=5)

        self.attach_btn = ctk.CTkButton(
            self,
            text="📎",
            width=45
        )
        self.attach_btn.pack(side="left", padx=5)

        self.voice_btn = ctk.CTkButton(
            self,
            text="🎤",
            width=45
        )
        self.voice_btn.pack(side="left", padx=5)

        self.send_btn = ctk.CTkButton(
            self,
            text="➤",
            width=60,
            command=self.send
        )

        self.send_btn.pack(
            side="right",
            padx=10
        )

    # -----------------------------
    # Enter Key
    # -----------------------------
    def on_enter(self, event):

        self.send()

        return "break"

    # -----------------------------
    # Send Message
    # -----------------------------
    def send(self):

        message = self.entry.get("1.0", "end").strip()

        if not message:
            return

        self.send_callback(message)

        self.entry.delete("1.0", "end")

    # -----------------------------
    # Enable / Disable
    # -----------------------------
    def disable(self):

        self.entry.configure(state="disabled")
        self.send_btn.configure(state="disabled")

    def enable(self):

        self.entry.configure(state="normal")
        self.send_btn.configure(state="normal")

        self.entry.focus()