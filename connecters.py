"""
@author: Abhilash Raj

Module containing connectors to Elasticsearch DB and Dropbox
"""

from dropbox import Dropbox # To connect to dropbox API
from configparser import RawConfigParser # To load configuration
from elasticsearch import Elasticsearch # ElasticSearch ORM

# Creating configparser object
config = RawConfigParser()

# loading the config file
config.read('config.ini')

# Extracting dropbox access token from configuration
dropbox_access_token = config.get('dropbox', 'access_token')

# Extracting elasticsearch cloud id
es_cloud_id = config.get('elasticsearch', 'cloud_id')

# Extracting elasticsearch credentials
es_username = config.get('elasticsearch', 'username')
es_password = config.get('elasticsearch', 'password')

# Creating Dropbox connector object
dbx = Dropbox(dropbox_access_token)

# Creating Elasticsearch connector object
es = Elasticsearch(
    cloud_id= es_cloud_id,
    http_auth=(es_username, es_password),
)
