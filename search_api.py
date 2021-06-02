"""
@author: Abhilash Raj

Module containing Backend API driver code
"""


from flask import Flask # For creating route and handling request
from flask import request # For accessing request strings
from dropbox_connect import get_dropbox_files # To retrieve file details from data
from db_connect import sync_db, search_db
from time import time
from logger import log

# Creating Flask object
app = Flask(__name__)

def create_response():
    '''Creates response template'''
    return {'Status': False}

@app.route('/search')
def search():
    '''API endpoint for searching phrase in DB'''

    log.info('Request received')

    # Checking no query in the request
    if 'q' not in request.args:
        log.error(f'No query found in request')

        # Creating custom response
        response = create_response()
        response['Message'] = 'No query in request'

        # Returning bad request response
        return response, 400

    # Extracting the search phrase from the query
    search_phrase = request.args.get('q').replace('"', '')
    log.info(f'Search query received for {search_phrase}')

    log.info('Searching the DB')
    # Calling the search function from db connect
    df_result, not_in_db = search_db(search_phrase)

    # If no files found in DB containing the text
    if df_result.empty and not_in_db:
        log.warning(f'No files found in db containing {search_phrase}')

        # Creating not found response
        response = create_response()
        response['Message'] = f'No files found containing {search_phrase}'
        response_code = 404

    # If error occured while searching
    elif df_result.empty and not not_in_db:

        log.error('Error while searching the DB')

        # Creating internal server error response
        response = create_response()
        response['Message'] = f'Error occured while searching {search_phrase}'
        response_code = 500

    else:
        # For files found containing the phrase in DB
        log.info(f'Files found containing {search_phrase}')

        # Creating successful response
        response = create_response()
        response['Status'] = True
        # Adding Data in the response as list of dict
        response['Data'] = df_result.to_dict('records')
        response_code = 200

    # Returning request successful response
    return response, response_code


if __name__ == '__main__':
    app.run(debug=True)
