import customtkinter as ctk


class InputBar(ctk.CTkFrame):

    def __init__(self, master, send_callback):
        super().__init__(master)

        self.pack(fill="x", padx=20, pady=15)

        self.send_callback = send_callback

        # -----------------------------
        # Message Box
        # -----------------------------
        self.entry = ctk.CTkTextbox(
            self,
            height=60,
            font=("Segoe UI", 15),
            wrap="word"
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(10, 5),
            pady=10
        )

        # Enter = Send
        self.entry.bind("<Return>", self.on_enter)

        # -----------------------------
        # Emoji Button
        # -----------------------------
        self.emoji_btn = ctk.CTkButton(
            self,
            text="😊",
            width=45
        )
        self.emoji_btn.pack(side="left", padx=5)

        # -----------------------------
        # Attachment Button
        # -----------------------------
        self.attach_btn = ctk.CTkButton(
            self,
            text="📎",
            width=45
        )
        self.attach_btn.pack(side="left", padx=5)

        # -----------------------------
        # Voice Button
        # -----------------------------
        self.voice_btn = ctk.CTkButton(
            self,
            text="🎤",
            width=45
        )
        self.voice_btn.pack(side="left", padx=5)

        # -----------------------------
        # Send Button
        # -----------------------------
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

        # Focus cursor
        self.entry.focus()

    # --------------------------------------------------
    # ENTER KEY
    # --------------------------------------------------

    def on_enter(self, event):

        # Shift + Enter = New Line
        if event.state & 0x0001:
            return

        self.send()

        return "break"

    # --------------------------------------------------
    # SEND MESSAGE
    # --------------------------------------------------

    def send(self):

        message = self.entry.get("1.0", "end-1c").strip()

        if not message:
            return

        # Clear textbox BEFORE callback
        self.entry.delete("1.0", "end")

        # Cursor back
        self.entry.focus()

        # Send message
        self.send_callback(message)

    # --------------------------------------------------
    # DISABLE INPUT
    # --------------------------------------------------

    def disable(self):

        self.entry.configure(state="disabled")
        self.send_btn.configure(state="disabled")

    # --------------------------------------------------
    # ENABLE INPUT
    # --------------------------------------------------

    def enable(self):

        self.entry.configure(state="normal")
        self.send_btn.configure(state="normal")

        self.entry.focus()