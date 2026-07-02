import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(self, master, new_chat_callback):
        super().__init__(
            master,
            width=240,
            corner_radius=0
        )

        self.pack_propagate(False)

        ctk.CTkLabel(
            self,
            text="🤖\nKrish AI",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=30)

        self.new_chat_btn = ctk.CTkButton(
            self,
            text="➕ New Chat",
            command=new_chat_callback
        )

        self.new_chat_btn.pack(
            fill="x",
            padx=15,
            pady=10
        )

        ctk.CTkLabel(
            self,
            text="Recent Chats",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=(25, 10))

        self.chat_list = ctk.CTkScrollableFrame(
            self,
            height=350
        )

        self.chat_list.pack(
            fill="both",
            expand=True,
            padx=10
        )

        ctk.CTkButton(
            self,
            text="⚙ Settings"
        ).pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=20
        )