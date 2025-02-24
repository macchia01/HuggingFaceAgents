import fitz  # PyMuPDF
import docx
import os
from smolagents.tools import Tool

class DocumentQATool(Tool):
    name = "document_qa"
    description = "Extracts answers from an uploaded document based on a question."
    inputs = {
        'document_path': {'type': 'string', 'description': 'Path to the uploaded document'},
        'question': {'type': 'string', 'description': 'Question about the document'}
    }
    output_type = "string"

    def forward(self, document_path: str, question: str) -> str:
        """Extracts relevant text from a document based on a question."""
        if not os.path.exists(document_path):
            return "Error: Document not found."

        text = self.extract_text(document_path)

        # Perform basic keyword matching (improve this with NLP models later)
        if question.lower() in text.lower():
            return f"Found reference: {text[:500]}..."  # Limit output to 500 characters
        return "No direct answer found. Try rephrasing."

    def extract_text(self, document_path):
        """Extracts text from PDF or DOCX files."""
        if document_path.endswith(".pdf"):
            return self.extract_pdf_text(document_path)
        elif document_path.endswith(".docx"):
            return self.extract_docx_text(document_path)
        return "Unsupported file type."

    def extract_pdf_text(self, pdf_path):
        """Extracts text from a PDF file."""
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text

    def extract_docx_text(self, docx_path):
        """Extracts text from a DOCX file."""
        doc = docx.Document(docx_path)
        return "\n".join([para.text for para in doc.paragraphs])
