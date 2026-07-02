import customtkinter as ctk


class InputBar(ctk.CTkFrame):

    def __init__(self, master, send_callback):
        super().__init__(master)

        self.pack(fill="x", padx=20, pady=15)

        self.send_callback = send_callback

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text="Type your message...",
            height=45,
            font=("Segoe UI", 15)
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(10, 5),
            pady=10
        )

        self.entry.bind("<Return>", lambda e: self.send())

        ctk.CTkButton(self, text="😊", width=45).pack(side="left", padx=5)
        ctk.CTkButton(self, text="📎", width=45).pack(side="left", padx=5)
        ctk.CTkButton(self, text="🎤", width=45).pack(side="left", padx=5)

        ctk.CTkButton(
            self,
            text="➤",
            width=60,
            command=self.send
        ).pack(side="right", padx=10)

    def send(self):

        message = self.entry.get().strip()

        if message == "":
            return

        self.send_callback(message)

        self.entry.delete(0, "end")