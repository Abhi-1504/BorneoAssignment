"""
@author: Abhilash Raj

Module containing connectors to Elasticsearch DB and Dropbox
"""

import json  # For parsing sync resolver
from dropbox import Dropbox  # To connect to dropbox API
from configparser import RawConfigParser  # To load configuration
from elasticsearch import Elasticsearch  # ElasticSearch ORM

# Creating configparser object
config = RawConfigParser()

# loading the config file
config.read("config.ini")

# Extracting dropbox access token from configuration
dropbox_access_token = config.get("dropbox", "access_token")

# Extracting elasticsearch endpoint
es_endpoint = config.get("elasticsearch", "end_point")

# Extracting elasticsearch credentials
es_username = config.get("elasticsearch", "username")
es_password = config.get("elasticsearch", "password")

# Extracting elasticsearch index_name
es_index_name = config.get("elasticsearch", "index_name")

# Extracting elasticsearch doc columns
columns = json.loads(config.get("elasticsearch", "doc_columns"))

# Extracting minutes for periodic interval of sync
minutes = int(config.get("interval", "minutes"))

# Creating Dropbox connector object
dbx = Dropbox(dropbox_access_token)

# Creating Elasticsearch connector object
es = Elasticsearch(es_endpoint, http_auth=("elastic", "HUbkdahmsWnFtmsMGv9fzBtC"))
