import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(self, master, new_chat_callback):
        super().__init__(
            master,
            width=240,
            corner_radius=0
        )

        self.pack_propagate(False)

        self.chat_buttons = {}

        ctk.CTkLabel(
            self,
            text="🤖\nKrish AI",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=30)

        self.new_chat_btn = ctk.CTkButton(
            self,
            text="➕ New Chat",
            command=new_chat_callback,
            height=45
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
            fg_color="transparent"
        )

        self.chat_list.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        self.settings_btn = ctk.CTkButton(
            self,
            text="⚙ Settings",
            height=45
        )

        self.settings_btn.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=20
        )

    def clear_chat_list(self):

        self.chat_buttons.clear()

        for widget in self.chat_list.winfo_children():
            widget.destroy()

    def add_chat_button(self, chat_id, title, command):

        button = ctk.CTkButton(
            self.chat_list,
            text=f"💬 {title}",
            anchor="w",
            command=command,
            height=38
        )

        button.pack(
            fill="x",
            pady=3
        )

        self.chat_buttons[chat_id] = button

    def highlight_chat(self, chat_id):

        for cid, button in self.chat_buttons.items():

            if cid == chat_id:
                button.configure(fg_color=("gray75", "gray30"))
            else:
                button.configure(fg_color=("gray85", "gray20"))