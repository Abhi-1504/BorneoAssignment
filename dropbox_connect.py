"""
@author: Abhilash Raj

Module containing helper functions for connecting to elastic search
"""
import pandas as pd
from connecters import dbx, columns
from io import BytesIO  # To store content of file in memory
from logger import log
from extract_text import extract_text_from_pdf, extract_text_from_docx

# This function is being called by dataframe apply method only
def __get_file_data(path):
    """Function retriving the dropbox file data
    Param(s):
        path (str)  :   Path of file in dropbox
    Returns(s):
        pd.Series (pandas.Series)   : Pandas Series consisting of file details
    """
    log.info(f"Fetching data for {path} file")
    # Extracting the file metadata and file
    metadata, file = dbx.files_download(path)

    log.info(f"Extracting text from {path} file")
    # Checking the file extension
    if metadata.name.split(".")[-1] == "pdf":
        # Extracting text from PDF file
        text = extract_text_from_pdf(BytesIO(file.content))

    elif metadata.name.split(".")[-1] == "docx":
        # Extracting text from docx file
        text = extract_text_from_docx(BytesIO(file.content))

    elif metadata.name.split(".")[-1] == "txt":
        # Extracting text from text file
        text = file.content.decode()

    log.info(f"Creating shareable link for {path} file")
    # Creating Shareable link for the file
    shareable_link = dbx.sharing_create_shared_link(path).url

    # returning pandas series
    return pd.Series([metadata.name, text, metadata.server_modified, shareable_link])


def get_dropbox_files():
    """Function to get all the file data from the dropbox
    Return(s):
        df_dbx (pandas.DataFrame) : Pandas DataFrame containining file data
    """

    log.info("Fetching data from dropbox")

    # Creating empty dataframe
    df_dbx = pd.DataFrame()

    try:
        # Getting the list of files in dropbox
        df_dbx[columns[-1]] = [
            file.path_display for file in dbx.files_list_folder("",).entries
        ]

        # Retriving all the required data for files
        df_dbx[columns[:-1]] = df_dbx[columns[-1]].apply(__get_file_data)

        # Re-arranging the dataframe columns
        df_dbx = df_dbx[columns]

        log.info("Fetching data from dropbox successful")

    except Exception as e:
        log.error(f"{str(e)}")
        log.error("Fetching data from dropbox failed")

    # Returning the dataframe
    return df_dbx