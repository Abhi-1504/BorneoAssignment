"""
@author: Abhilash Raj

Module containing Backend API driver code
"""


from flask import Flask # For creating route and handling request
from flask import request # For accessing request strings

# Creating Flask object
app = Flask(__name__)

@app.route('/search')
def search():
    search_phrase = request.args.get('q').replace('"','')
    return f'<h1>{search_phrase}</h1>'


if __name__ == '__main__':
    app.run(debug=True)
