import customtkinter as ctk

from components.syntax_highlighter import SyntaxHighlighter


class CodeBlock(ctk.CTkFrame):

    def __init__(self, master, code, language="text"):
        super().__init__(
            master,
            fg_color=("#F4F4F4", "#1E1E1E"),
            corner_radius=12,
            border_width=1,
            border_color=("#D0D0D0", "#333333")
        )

        self.code = code
        self.language = language.lower()

        self.highlighter = SyntaxHighlighter()

        # ====================================
        # Header
        # ====================================

        header = ctk.CTkFrame(
            self,
            fg_color=("#E8E8E8", "#2D2D2D"),
            corner_radius=10,
            height=36
        )

        header.pack(
            fill="x",
            padx=2,
            pady=(2, 0)
        )

        title = ctk.CTkLabel(
            header,
            text=self.language.upper(),
            font=("Segoe UI", 12, "bold")
        )

        title.pack(
            side="left",
            padx=12
        )

        self.copy_btn = ctk.CTkButton(
            header,
            text="📋 Copy",
            width=90,
            height=28,
            font=("Segoe UI", 11),
            command=self.copy_code
        )

        self.copy_btn.pack(
            side="right",
            padx=8,
            pady=4
        )

        # ====================================
        # Code Viewer
        # ====================================

        self.textbox = ctk.CTkTextbox(
            self,
            wrap="none",
            height=220,
            font=("Consolas", 13)
        )

        self.textbox.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        self.textbox.insert(
            "1.0",
            code
        )

        self.apply_highlighting()

        self.textbox.configure(
            state="disabled"
        )

    # ====================================
    # Syntax Highlighting
    # ====================================

    def apply_highlighting(self):

        tokens = self.highlighter.highlight(
            self.code,
            self.language
        )

        self.textbox.delete(
            "1.0",
            "end"
        )

        # Token colors
        colors = {

            "Token.Keyword": "#569CD6",
            "Token.Name.Function": "#DCDCAA",
            "Token.Name.Class": "#4EC9B0",
            "Token.Literal.String": "#CE9178",
            "Token.Comment": "#6A9955",
            "Token.Literal.Number": "#B5CEA8",
            "Token.Operator": "#D4D4D4"

        }

        for token, value in tokens:

            tag = str(token)

            self.textbox.insert(
                "end",
                value,
                tag
            )

            self.textbox.tag_config(
                tag,
                foreground=colors.get(
                    tag,
                    "#D4D4D4"
                )
            )

    # ====================================
    # Copy
    # ====================================

    def copy_code(self):

        self.clipboard_clear()
        self.clipboard_append(self.code)

        self.copy_btn.configure(
            text="✅ Copied"
        )

        self.after(
            1500,
            lambda: self.copy_btn.configure(
                text="📋 Copy"
            )
        )