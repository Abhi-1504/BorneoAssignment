# BorneoAssignment
------------------

The repository consist of the solution for Borneo.io Python Developer Assignment.
The solution is written in Python 3 language and requires some additional libraries to be installed.

## Table of contents
--------------------

* config.ini
* logger.py
* connecters.py
* db_connect.py
* dropbox_connect.py
* search_api.py
* extract_text.py


## Dependencies
---------------

The solution is using following python modules:

* io
* os
* docx
* flask
* logging
* pdftotext
* configparser

## Configuration
----------------

In config.ini file the following configuration needs to be done:

* access_token  : Dropbox Access Token generated for a dropbox folder or full dropbox with correct permissions (_share.write_, _files.metadata.read_ and _files.content.read_)
* end_point     : Elasticsearch Cloud endpoint
* username      : Elasticsearch Username
* password      : Elasticsearch Password

## Files
--------

* config.ini          : Configuration file
* connectors.py       : Module creating connector objects and constants for Elasticsearch DB and Dropbox from configuration
* search_api.py       : Main driver script to run the backend search API
* extarct_text.py     : Module containing functions to extract text from docx, pdf and txt files
* logger.py           : Module containing logger
* db_connect.py       : Module containing functions to perform elasticsearch related operations
* dropbox_connect.py  : Module containing functions to perform dropbox related operations
