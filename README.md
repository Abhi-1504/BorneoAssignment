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
* templates
* forms.py
* search_ui.py
* sync_resolver.json
* synchronizing_data.py


## Dependencies
---------------

The solution is using following python modules:

* io
* os
* docx
* json
* flask
* pandas
* logging
* dropbox
* datetime
* pdftotext
* apscheduler
* configparser
* elasticsearch

## Configuration
----------------

In config.ini file the following configuration needs to be done:

* minutes       : Interval in which the synchronization needs to happen
* access_token  : Dropbox Access Token generated for a dropbox folder or full dropbox with correct permissions (_share.write_, _files.metadata.read_ and _files.content.read_)
* end_point     : Elasticsearch Cloud endpoint
* username      : Elasticsearch Username
* password      : Elasticsearch Password
* index_name    : Elasticsearch index name
* doc_columns   : Configures Elasticsearch index doc attributes. Values inside the double quotes *__("")__* needs to be replaced by the desired column names. This setup is done to remove sequential dependencies on the column and to minimize the hardcoding of column names and changes required to make in future

## Files
--------

* config.ini              : Configuration file
* connectors.py           : Module creating connector objects and constants for Elasticsearch DB and Dropbox from configuration
* search_api.py           : Main driver script to run the backend search API
* extarct_text.py         : Module containing functions to extract text from docx, pdf and txt files
* logger.py               : Module containing logger
* db_connect.py           : Module containing functions to perform elasticsearch related operations
* dropbox_connect.py      : Module containing functions to perform dropbox related operations
* sync_resolver.json      : JSON file being used and synchronization resolver
* synchronizing_data.py   : Module containing synchronization of data and create response related functions
* search_ui.py            : Module driver script to run frontend search UI
* templates               : Directory containing Jinja templates for frontend
* unittest_search_api.py  : Module containing unit testing of search api endpoints


## NOTE to Evaluator
--------------------

To extract text from pdf, the solution is using pdftotext library, which is capable of extracting text from most of the pdf files. But since pdf has various types of encoding so their is a chance that the library won't be able to extract correctly encoded text from the all the pdf files.  
