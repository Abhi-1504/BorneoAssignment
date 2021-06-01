"""
@author: Abhilash Raj

Module containing helper methods for extracting text from pdf and docx files
"""

from io import BytesIO # To store content of file in memory
from pdftotext import PDF # For extracting text from PDF files
from docx import Document # For extracting text from docx files


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
    text = '\n'.join(list(pdf_content))

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
    text = '\n'.join([para.text for para in docx_content.paragraphs])

    # Returning the text
    return text



def extract_text(files_data):
    """Extract text from pdf, and docx files
    Param(s):
        file_data (list)        :   List of file name, file content and date
    Return(s):
        files_text (dict)       :   list of file data
    """

    # List to store file name and text
    files_text = []
    for filename, file_content, date in files_data:

        # Checking the file extension
        # For docx
        if filename.split('.')[-1] == 'docx':

            # Calling extract_text_from_docx to extract text from docx file
            text = extract_text_from_docx(BytesIO(file_content))

        # For pdf
        elif filename.split('.')[-1] == 'pdf':

            # Calling extract_text_from_pdf to extract text from pdf file
            text = extract_text_from_pdf(BytesIO(file_content))

        # For txt
        elif filename.split('.')[-1] == 'txt':
            text = str(file_content)

        # For others
        else:

            # Setting text to unsupported in case of any other file type
            text = 'Unsupported'

        # Adding file name and text into the List
        files_text.append([filename, text, date])

    return files_text
