import customtkinter as ctk
from tkinter import filedialog, messagebox


class InputBar(ctk.CTkFrame):

    def __init__(
        self,
        master,
        send_callback,
        pdf_callback=None
    ):
        super().__init__(master)

        self.pack(fill="x", padx=20, pady=15)

        self.send_callback = send_callback
        self.pdf_callback = pdf_callback

        # --------------------------------
        # Message Box
        # --------------------------------

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

        self.entry.bind(
            "<Return>",
            self.on_enter
        )

        # --------------------------------
        # Emoji
        # --------------------------------

        self.emoji_btn = ctk.CTkButton(
            self,
            text="😊",
            width=45
        )

        self.emoji_btn.pack(
            side="left",
            padx=4
        )

        # --------------------------------
        # PDF Upload
        # --------------------------------

        self.attach_btn = ctk.CTkButton(
            self,
            text="📎",
            width=45,
            command=self.attach_pdf
        )

        self.attach_btn.pack(
            side="left",
            padx=4
        )

        # --------------------------------
        # Voice
        # --------------------------------

        self.voice_btn = ctk.CTkButton(
            self,
            text="🎤",
            width=45
        )

        self.voice_btn.pack(
            side="left",
            padx=4
        )

        # --------------------------------
        # Web Search Switch
        # --------------------------------

        self.web_switch = ctk.CTkSwitch(
            self,
            text="🌐 Web"
        )

        self.web_switch.pack(
            side="left",
            padx=10
        )

        # --------------------------------
        # Send
        # --------------------------------

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

        self.entry.focus()

    # --------------------------------

    def is_web_enabled(self):

        return bool(
            self.web_switch.get()
        )

    # --------------------------------

    def attach_pdf(self):

        file_path = filedialog.askopenfilename(

            title="Select PDF",

            filetypes=[
                ("PDF Files", "*.pdf")
            ]
        )

        if not file_path:
            return

        if self.pdf_callback:

            self.pdf_callback(file_path)

        messagebox.showinfo(

            "PDF Loaded",

            "PDF loaded successfully."

        )

    # --------------------------------

    def on_enter(self, event):

        if event.state & 0x0001:
            return

        self.send()

        return "break"

    # --------------------------------

    def send(self):

        message = self.entry.get(
            "1.0",
            "end-1c"
        ).strip()

        if not message:
            return

        self.entry.delete(
            "1.0",
            "end"
        )

        self.entry.focus()

        self.send_callback(message)

    # --------------------------------

    def disable(self):

        self.entry.configure(
            state="disabled"
        )

        self.send_btn.configure(
            state="disabled"
        )

    # --------------------------------

    def enable(self):

        self.entry.configure(
            state="normal"
        )

        self.send_btn.configure(
            state="normal"
        )

        self.entry.focus()