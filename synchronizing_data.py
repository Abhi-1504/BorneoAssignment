"""
@author: Abhilash Raj

Module containing Data Synchronization and response creation related functions
"""

import json  # For updating syncronization resolver
from db_connect import sync_db  # For synchronizing elasticsearch DB
from connecters import minutes  # For setting the sync minute
from datetime import datetime as dt  # For timestamp
from logger import log  # For logging
from dropbox_connect import get_dropbox_files  # For dropbox operations


def create_response(status, message, response_code):
    """Creates response template
    Return(s):
        response (dict) : response template
    """
    log.info("Creating response")
    return {"Status": status, "Message": message}, response_code


def sync_resolve(update=False, updated_sync_resolver=None):
    """Synchronization resolver for multiple sync requests
    Param(s):
        update (bool)                   : To check if sync resolver needs to be updated
        updated_sync_resolver (dict)    : updated syncronization resolver
    Return(s):
        sync_resolver (dict)            : Current sync resolver
    """
    try:
        # If the current status of sync resolver needs to be updated
        if update:
            log.info("Updating the syncronization resolver")
            with open("sync_resolver.json", "w") as f:
                json.dump(updated_sync_resolver, f, indent=4)

        # For returning the current state of the synchronization resolver
        else:
            log.info("Loading the current synchronization resolver")
            with open("sync_resolver.json") as f:
                sync_resolver = json.load(f)

            return sync_resolver

    except Exception as e:
        log.error(f"{str(e)}")
        return {}


def sync_data(request_time=None):

    sync_resolver = sync_resolve()

    try:
        if len(sync_resolver) == 0:
            log.error("Updating/Loading Synchronization resolver failed")
            raise ValueError

        # For first time run of the sync api
        if "Sync Stop Time" in sync_resolver.keys() and request_time != None:
            last_sync_time = dt.fromisoformat(sync_resolver["Sync Stop Time"])
            time_diff = (request_time - last_sync_time).seconds / 60
        else:
            time_diff = minutes / 2

        ## Synchronization resquest resolver block

        # For request received in between synchronization
        if sync_resolver["Synchronizing"]:
            log.warning("Synchronization already in progress")
            response = create_response(
                False, "Synchronizing already in Progress! Please wait...", 409
            )

        # For request recieved for time less than the half of periodic sync of DB
        elif request_time != None and time_diff < (minutes / 2):
            log.warning("Synchronization recently finished")
            response = create_response(
                False, "Syncronization recently completed. Try again later", 406
            )

        # For triggering synchronization
        else:
            log.info("Synchronization Started")
            sync_resolver["Synchronizing"] = True
            sync_resolver["Sync Start Time"] = dt.now().isoformat()

            # In case for first time run
            try:
                sync_resolver.pop("Sync Stop Time")
            except:
                pass
            # Blocking the resource during refreshing DB
            sync_resolve(True, sync_resolver)

            # Getting all the file details
            log.info("Fetching data from dropbox")
            df_dbx, status = get_dropbox_files()

            # Updating DB
            log.info("Synchronizing the DB")
            if df_dbx.empty and status:
                sync_db()
            elif df_dbx.empty and not status:
                # Releasing the resource because of failure
                sync_resolver["Synchronizing"] = False
                sync_resolver["Sync Stop Time"] = dt.now().isoformat()
                sync_resolve(True, sync_resolver)
                raise ValueError
            else:
                sync_db(df_dbx)

            # Releasing the resource after update
            sync_resolver["Synchronizing"] = False
            sync_resolver["Sync Stop Time"] = dt.now().isoformat()
            sync_resolve(True, sync_resolver)

            log.info("Synchronization completed")

            response = create_response(
                True, "Syncronization completed Successfully", 200
            )

    except Exception as e:
        log.error(f"{str(e)}")

        # Resstting the sync resolver to initial value
        response = create_response(False, "Syncronisation Failed", 500)
        with open("sync_resolver.json", "w") as f:
            json.dump({"Synchronizing": False}, f, indent=4)

    return response


if __name__ == "__main__":
    print(sync_data())
