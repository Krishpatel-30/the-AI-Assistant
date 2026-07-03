from pypdf import PdfReader
from rag import RAG


class PDFChat:

    def __init__(self):

        self.pdf_path = None
        self.pages = []
        self.full_text = ""

        # RAG Engine
        self.rag = RAG()

    # -------------------------------------------------
    # Load PDF
    # -------------------------------------------------

    def load_pdf(self, file_path):

        self.pdf_path = file_path

        self.pages = []

        self.full_text = ""

        reader = PdfReader(file_path)

        for page in reader.pages:

            text = page.extract_text()

            if text is None:
                text = ""

            self.pages.append(text)

        self.full_text = "\n\n".join(self.pages)

        # Build Vector Database
        self.rag.build(self.full_text)

        return len(self.pages)

    # -------------------------------------------------
    # Search PDF
    # -------------------------------------------------

    def search(self, question, top_k=5):

        return self.rag.search(
            question,
            top_k
        )

    # -------------------------------------------------
    # Get Relevant Context
    # -------------------------------------------------

    def get_context(self, question):

        chunks = self.search(question)

        return "\n\n".join(chunks)

    # -------------------------------------------------
    # Get Complete Text
    # -------------------------------------------------

    def get_text(self):

        return self.full_text

    # -------------------------------------------------
    # Get One Page
    # -------------------------------------------------

    def get_page(self, page_number):

        if page_number < 1:
            return ""

        if page_number > len(self.pages):
            return ""

        return self.pages[page_number - 1]

    # -------------------------------------------------
    # Page Count
    # -------------------------------------------------

    def page_count(self):

        return len(self.pages)

    # -------------------------------------------------
    # Loaded?
    # -------------------------------------------------

    def is_loaded(self):

        return self.pdf_path is not None