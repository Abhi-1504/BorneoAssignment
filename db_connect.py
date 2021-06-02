"""
@author: Abhilash Raj

Module containing helper functions for connecting to elastic search
"""

from connecters import es, es_index_name
from datetime import datetime
from logger import log


def search_db(search_phrase):
    pass


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
                lambda row: es.index(index=es_index_name, body=row.to_dict()),
                axis=1
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
