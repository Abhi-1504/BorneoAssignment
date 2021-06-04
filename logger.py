"""
@author: Abhilash Raj

Module to create logger for all modules used
and log file directory
"""

import os  # For System Path
import logging  # For logging
from datetime import datetime  # For creating logs based on date

# Today's date as string
today = datetime.today().strftime("%Y-%m-%d")

# Creating directory to store log
if not os.path.exists("logs"):
    os.mkdir("logs")

# Format for logging
formatter = "%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(message)s"

# Setting up logger based on date
logging.basicConfig(
    format=formatter,
    level=logging.INFO,
    filename=os.path.join(os.getcwd(), f"logs/search_api_{today}.log"),
    filemode="a",
)

log = logging.getLogger()
