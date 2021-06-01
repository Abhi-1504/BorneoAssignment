# BorneoAssignment
------------------

The repository consist of the solution for Borneo.io Python Developer Assignment.
The solution is written in Python 3 language and requires some additional libraries to be installed.

## Table of contents
--------------------

* config.ini
* connecters.py
* search_api.py
* extract_text.py

## Dependencies
---------------

The solution is using following python modules:

* io
* docx
* flask
* pdftotext

## Configuration
----------------

In config.ini file the following configuration needs to be done:

* access_token  : Dropbox Access Token generated with correct permissions (_share.write_, _files.metadata.read_ and _files.content.read_)
* cloud_id      : Elasticsearch Cloud ID
* username      : Elasticsearch Username
* password      : Elasticsearch Password

## Files
--------

* config.ini      : Configuration file
* connectors.py   : Module creating connectors object for Elasticsearch DB and Dropbox
* search_api.py   : Main driver script to run the backend search API
* extarct_text.py : Module containing functions to extract text from docx, pdf and txt files
