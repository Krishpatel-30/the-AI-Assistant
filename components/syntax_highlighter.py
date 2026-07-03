from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.lexers.special import TextLexer


class SyntaxHighlighter:

    def highlight(self, code, language="text"):

        try:
            lexer = get_lexer_by_name(language)

        except Exception:
            lexer = TextLexer()

        return list(
            lex(code, lexer)
        )