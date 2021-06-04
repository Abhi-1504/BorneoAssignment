"""
@author: Abhilash Raj

Module containing helper functions for connecting to elastic search
"""

from datetime import datetime  # For datetime
from logger import log  # For logging
import pandas as pd  # For storing data
from connecters import es, es_index_name, columns  # For elasticsearch connecters


def search_db(search_phrase):
    """Searches the phrase in file text in the elasticsearch index
    Param(s):
        search_phrase (str)     :   Search Phrase that needs to be search in the index
    Return(s):
        df,True/False (tuple)   :   Returns a tuple consiting of Pandas DataFrame and boolean value indicating if not found in DB
    """
    # Creating empty DataFrame
    df = pd.DataFrame()
    try:

        log.info("Creating query to perform the search")
        # Creating query for searching Elasticsearch
        query = {
            "_source": [columns["FILE_NAME"], columns["SHAREABLE_LINK"]],
            "query": {
                "match": {columns["FILE_TEXT"]: "*" + search_phrase.lower() + "*"}
            },
        }

        log.info(f"Searching the DB for {search_phrase}")
        # query the db to search for the phrase
        result = es.search(index=es_index_name, body=query)

        # Checking if no matches found
        if len(result["hits"]["hits"]) == 0:
            log.info(f"No matches for {search_phrase}")
            return df, True

        log.info("Matches found in the DB")
        # Extracting the required data from response
        required_data = [data["_source"] for data in result["hits"]["hits"]]

        # Returning the extracted data
        return df.append(required_data, ignore_index=True), False

    except Exception as e:
        log.error(f"{str(e)}")
        log.error(f"Search for {search_phrase} in DB failed")
        return df, False


def sync_db(df_dbx=None):
    """Synchronizes Elasticsearch Index with dropbox data
    Param(s):
        df_dbx (pandas.DataFrame)   :   Pandas DataFrame consisting of dropbox file data
    Return(s):
        True/None (bool/NoneType)   :   True on successful synchronization else None
    """
    try:
        log.info("Synchronizing the dropbox files with DB")
        # Creating index in Elasticsearch if not present
        if es_index_name not in es.indices.get_alias("*").keys():
            es.indices.create(es_index_name)

        log.info("Deleting the previous data from DB")
        # Deleting the data in the index
        es.delete_by_query(index=es_index_name, body={"query": {"match_all": {}}})
        log.info("Deletion completed")

        # Updating the index
        log.info("Updating the DB with the dropbox files data")
        if isinstance(df_dbx, pd.DataFrame):
            # Adding the Synced On column with current timestamp
            df_dbx["Synced On"] = datetime.now()

            # Updating the new data in the elasticsearch index using apply method
            df_dbx.apply(
                lambda row: es.index(index=es_index_name, body=row.to_dict()), axis=1
            )
            log.info("Update of DB completed")

        else:
            log.info("No data to add to the DB. Check if Dropbox is empty")

        log.info("Synchronization of dropbox with DB successful")
        # returning True on successful sync
        return True
    except Exception as e:
        log.error(f"{str(e)}")
        log.error("Synchronization of dropbox with DB failed")
