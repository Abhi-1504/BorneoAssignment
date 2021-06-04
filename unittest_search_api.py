"""
@author: Abhilash Raj

Module to unit test search api
"""

import json
import unittest
import requests
import os
from datetime import datetime as dt
from synchronizing_data import sync_resolve, create_response


class TestSearchAPI(unittest.TestCase):
    """Class to unit test search API"""

    @classmethod
    def setUpClass(cls):
        """Class method called once before the testing start"""
        # base url for search api
        base_url = "http://127.0.0.1:3000/{}"

        # endpoint for sync
        cls.sync_url = base_url.format("sync")

        # endpoint for search
        cls.search_url = base_url.format("search")

    def test_1_sync_failure(self):
        """Test case for synchronization failure"""

        # Emptying the sync_resolver
        with open("sync_resolver.json", "w") as f:
            json.dump({}, f, indent=4)

        # Sending Synchronization request
        response = requests.get(TestSearchAPI.sync_url)
        received_response = response.json()
        expected_response = create_response(False, "Syncronisation Failed", 500)[0]

        # Testing response code
        self.assertEqual(500, response.status_code)

        # Testing the response content
        self.assertDictEqual(expected_response, received_response)

    def test_2_sync_initial(self):
        """Test case for first time synchronization"""

        # Resetting Syncronisation resolver
        with open("sync_resolver.json", "w") as f:
            json.dump({"Synchronizing": False}, f, indent=4)

        # Sending Synchronization request
        response = requests.get(TestSearchAPI.sync_url)
        received_response = response.json()
        expected_response = create_response(
            True, "Syncronization completed Successfully", 200
        )[0]
        # Testing response code
        self.assertEqual(200, response.status_code)

        # Testing the response content
        self.assertDictEqual(expected_response, received_response)

    def test_3_sync_in_progress(self):
        """Test case for sync request during synchronization"""

        # Resetting the Syncronisation resolver to True
        with open("sync_resolver.json", "r") as f:
            sync_resolver = json.load(f)

        sync_resolver["Synchronizing"] = True
        with open("sync_resolver.json", "w") as f:
            json.dump(sync_resolver, f, indent=4)

        # Sending Synchronization request
        response = requests.get(TestSearchAPI.sync_url)
        received_response = response.json()
        expected_response = create_response(
            False, "Synchronizing already in Progress! Please wait...", 409
        )[0]

        # Testing response code
        self.assertEqual(409, response.status_code)

        # Testing the response content
        self.assertDictEqual(expected_response, received_response)

        # Reverting back the changes in the resolver
        sync_resolver["Synchronizing"] = False
        with open("sync_resolver.json", "w") as f:
            json.dump(sync_resolver, f, indent=4)

    def test_4_sync_request_blocked(self):
        """Test case to block the sync request if request time interval less than half of the interval"""

        # Sending Synchronization request
        response = requests.get(TestSearchAPI.sync_url)
        received_response = response.json()
        expected_response = create_response(
            False, "Syncronization recently completed. Try again later", 406
        )[0]

        # Testing response code
        self.assertEqual(406, response.status_code)

        # Testing the response content
        self.assertDictEqual(expected_response, received_response)

    def test_5_search_failure(self):
        """Test case for failure of search request"""

        # Sending search request without param
        response = requests.get(TestSearchAPI.search_url)
        received_response = response.json()
        expected_response = create_response(False, "No query in request", 400)[0]

        # Testing response code
        self.assertEqual(400, response.status_code)

        # Testing the response content
        self.assertDictEqual(expected_response, received_response)

        # Sending search request with empty param
        response = requests.get(TestSearchAPI.search_url, params={"q": ""})
        received_response = response.json()
        expected_response = create_response(False, "No value in query", 400)[0]

        # Testing response code
        self.assertEqual(400, response.status_code)

        # Testing the response content
        self.assertDictEqual(expected_response, received_response)

    def test_6_search_no_matches(self):
        """Test case for no matches found"""

        # Search token
        search_phrase = " a,jhvcaivh ilahvbihs bihs"

        # Sending search request with param
        response = requests.get(TestSearchAPI.search_url, params={"q": search_phrase})
        received_response = response.json()
        expected_response = create_response(
            False, f"No files found containing {search_phrase}", 404
        )[0]

        # Testing response code
        self.assertEqual(404, response.status_code)

        # Testing the response content
        self.assertDictEqual(expected_response, received_response)

    def test_7_search_matches_found(self):
        """Test case for matches found"""

        # Search token
        search_phrase = "the"

        # Sending search request with param
        response = requests.get(TestSearchAPI.search_url, params={"q": search_phrase})
        received_response = response.json()
        expected_response = create_response(True, "Matches Found", 200)[0]

        # Testing response code
        self.assertEqual(200, response.status_code)

        # Testing the response content
        self.assertDictEqual(expected_response, received_response)

    def test_8_search_during_sync_on(self):
        """Test case for searching while synchronizing was on"""

        # Search token
        search_phrase = "the"

        # Changing the sync_resolver state
        with open("sync_resolver.json") as f:
            sync_resolver = json.load(f)

        sync_resolver["Synchronizing"] = True

        with open("sync_resolver.json", "w") as f:
            json.dump(sync_resolver, f, indent=4)

        # Sending search request with param
        response = requests.get(TestSearchAPI.search_url, params={"q": search_phrase})
        received_response = response.json()
        expected_response = create_response(
            False, "Data Synchronizing in Progress, try after sometime.", 423
        )[0]

        # Testing response code
        self.assertEqual(423, response.status_code)

        # Testing the response content
        self.assertDictEqual(expected_response, received_response)

        # Reverting back the sync_resolver
        sync_resolver["Synchronizing"] = False
        with open("sync_resolver.json", "w") as f:
            json.dump(sync_resolver, f, indent=4)


if __name__ == "__main__":
    unittest.main()
