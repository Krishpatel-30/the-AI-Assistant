import re


class MarkdownRenderer:

    def __init__(self):
        pass

    def render(self, text):

        # Bold
        text = re.sub(
            r"\*\*(.*?)\*\*",
            r"🟦 \1",
            text
        )

        # Italic
        text = re.sub(
            r"\*(.*?)\*",
            r"\1",
            text
        )

        # Headers
        text = re.sub(
            r"^### (.*)$",
            r"\n🔹 \1",
            text,
            flags=re.MULTILINE
        )

        text = re.sub(
            r"^## (.*)$",
            r"\n🔷 \1",
            text,
            flags=re.MULTILINE
        )

        text = re.sub(
            r"^# (.*)$",
            r"\n🔵 \1",
            text,
            flags=re.MULTILINE
        )

        # Bullet lists
        text = re.sub(
            r"^- ",
            "• ",
            text,
            flags=re.MULTILINE
        )

        return text