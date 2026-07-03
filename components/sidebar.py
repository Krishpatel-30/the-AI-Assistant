import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(
        self,
        master,
        new_chat_callback,
        rename_callback=None,
        delete_callback=None
    ):
        super().__init__(
            master,
            width=260,
            corner_radius=0
        )

        self.pack_propagate(False)

        self.rename_callback = rename_callback
        self.delete_callback = delete_callback

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
            padx=10
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

    # ------------------------------------

    def clear_chat_list(self):

        self.chat_buttons.clear()

        for widget in self.chat_list.winfo_children():
            widget.destroy()

    # ------------------------------------

    def add_chat_button(
        self,
        chat_id,
        title,
        command
    ):

        row = ctk.CTkFrame(
            self.chat_list,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            pady=3
        )

        btn = ctk.CTkButton(
            row,
            text=f"💬 {title}",
            anchor="w",
            command=command,
            height=38
        )

        btn.pack(
            side="left",
            fill="x",
            expand=True
        )

        edit = ctk.CTkButton(
            row,
            text="✏️",
            width=32,
            height=32,
            command=lambda: (
                self.rename_callback(chat_id)
                if self.rename_callback
                else None
            )
        )

        edit.pack(
            side="left",
            padx=(4, 2)
        )

        delete = ctk.CTkButton(
            row,
            text="🗑️",
            width=32,
            height=32,
            fg_color="#b91c1c",
            hover_color="#991b1b",
            command=lambda: (
                self.delete_callback(chat_id)
                if self.delete_callback
                else None
            )
        )

        delete.pack(side="left")

        self.chat_buttons[chat_id] = btn

    # ------------------------------------

    def highlight_chat(self, chat_id):

        for cid, btn in self.chat_buttons.items():

            if cid == chat_id:

                btn.configure(
                    fg_color="#2563EB"
                )

            else:

                btn.configure(
                    fg_color=("gray85", "gray20")
                )