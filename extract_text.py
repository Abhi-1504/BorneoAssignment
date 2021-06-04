"""
@author: Abhilash Raj

Module containing helper functions for extracting text from pdf and docx files
"""

from pdftotext import PDF  # For extracting text from PDF files
from docx import Document  # For extracting text from docx files


def extract_text_from_pdf(pdf_memory_file):
    """Extract texts from pdf file content
    Param(s):
        pdf_memory_file (BytesIO)  : pdf file content as memory file
    Return(s):
        text (str)                 : text extracted from pdf file content
    """
    # Extracting the content of the memory file
    pdf_content = PDF(pdf_memory_file)

    # Converting the content into a list and joining it with newline
    # Extracting text from the pdf file content
    text = "\n".join(list(pdf_content))

    # Returning the text
    return text


def extract_text_from_docx(docx_memory_file):
    """Extract texts from docx file content
    Param(s):
        docx_memory_file (BytesIO)  : docx file content as memory file
    Return(s):
        text (str)                  : text extracted from docx file content
    """

    # Extracting the content of the memory file
    docx_content = Document(docx_memory_file)

    # Extracting the text from the paragraphs
    # Joining the texts using new line
    text = "\n".join([para.text for para in docx_content.paragraphs])

    # Returning the text
    return text
