"""
@author: Abhilash Raj

Module containing Backend API driver code
"""


from flask import Flask # For creating route and handling request
from flask import request # For accessing request strings
from dropbox_connect import get_dropbox_files # To retrieve file details from data
from time import time

# Creating Flask object
app = Flask(__name__)

@app.route('/search')
def search():
    if 'q' in request.args:
        search_phrase = request.args.get('q').replace('"', '')
        return search_phrase
    else:
        return 'No search phrase given'

if __name__ == '__main__':
    app.run(debug=True)
