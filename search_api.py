"""
@author: Abhilash Raj

Module containing Backend API driver code
"""

import json
from flask import Flask  # For creating route and handling request
from flask import request  # For accessing request queries
from connecters import minutes  # minutes for periodic interval of sync
from db_connect import search_db  # For elasticsearch operations
from datetime import datetime as dt  # For Synchronizing time
from synchronizing_data import sync_data, create_response  # For Syncing data
from apscheduler.schedulers.background import (
    BackgroundScheduler,
)  # For Sceduling synchronizer

# Creating Flask object
app = Flask(__name__)

# Creating Scheduler
sched = BackgroundScheduler(daemon=True)
sched.add_job(sync_data, "interval", minutes=minutes)
sched.start()


def logger():
    """Creates logger
    Return(s):
        log (logging)   :   logger for genearing logs
    """
    from logger import log

    return log


## REST API END-POINTS
@app.route("/sync")
def sync():
    """API endpoint for synchronizing data"""
    log = logger()
    request_time = dt.now()
    log.info(f"Synchronisation request received at {request_time.isoformat()}")
    log.info("Processing Syncronisation request")
    response = sync_data(request_time)
    log.info("Syncronisation request processed")
    return response


@app.route("/search")
def search():
    """API endpoint for searching phrase in DB"""
    # loading logger
    log = logger()

    log.info("Request received")

    # Checking no query in the request
    if "q" not in request.args:
        log.error(f"No query found in request")

        # Creating bad request response
        return create_response(False, "No query in request", 400)

    # Extracting the search phrase from the query
    search_phrase = request.args.get("q").replace('"', "")
    log.info(f"Search query received for {search_phrase}")

    # Checking if the search_phrase is empty
    if search_phrase == "":
        log.error(f"No search phrase in query")

        # Creating bad request response
        return create_response(False, "No value in query", 400)

    log.info("Searching the DB")
    # Calling the search function from db connect
    df_result, not_in_db = search_db(search_phrase)

    # If no files found in DB containing the text
    if df_result.empty and not_in_db:
        log.warning(f"No files found in db containing {search_phrase}")

        # Creating not found response
        response = create_response(
            False, f"No files found containing {search_phrase}", 404
        )

    # If error occured while searching
    elif df_result.empty and not not_in_db:

        log.error("Error while searching the DB")

        # Creating internal server error response
        response = create_response(
            False, f"Error occured while searching {search_phrase}", 500
        )

    else:
        # For files found containing the phrase in DB
        log.info(f"Files found containing {search_phrase}")

        # Creating successful response
        resp, resp_code = create_response(True, "Matches Found", 200)
        # Adding Data in the response as list of dict
        resp["Data"] = df_result.to_dict("records")
        # Creating response
        response = resp, resp_code

    # Returning request successful response
    return response


if __name__ == "__main__":
    app.run(debug=True, port=3000)
