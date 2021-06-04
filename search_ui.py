"""
@author: Abhilash Raj

Module containing Frontend UI driver code
"""

import requests
from forms import SearchForm
from flask import Flask, render_template, request, flash
from connecters import columns


# Creating Flask object
ui_app = Flask(__name__)

# Assigning long string as secret key for form verification
ui_app.config["SECRET_KEY"] = b"6dfc2d41c7d4b52de99292b60c98f8feb91da1a2a4b4f48a"

# Search Page
@ui_app.route("/", methods=["GET", "POST"])
@ui_app.route("/home", methods=["GET", "POST"])
def home():
    """Renders UI for search"""

    # Creating form object
    form = SearchForm()

    # Variable to store file data
    data = None

    # On Form submission (POST request)
    if request.method == "POST" and form.validate_on_submit():

        # Extracting the search token entered in the Input text field
        search_phrase = form.search_field.data

        # Sending GET request to the backend API with the search token in query
        response = requests.get(
            "http://localhost:3000/search", params={"q": search_phrase}
        )

        # Extracting the required respinse from the API
        resp = response.json()

        # Checking for DB syncronization or file not found response
        if not resp["Status"] and response.status_code in [404, 423]:
            # Creating Warning Alert message
            flash(resp["Message"], "warning")

        # Checking for any other failure response
        elif not resp["Status"]:
            # Creating Danger Alert message
            flash(flash(resp["Message"], "danger"))

        # For file matches found
        else:
            flash(resp["Message"], "success")

            # Extrcating the requuired file data
            data = [
                (ele[columns["FILE_NAME"]], ele[columns["SHAREABLE_LINK"]])
                for ele in resp["Data"]
            ]

    # Rendering the template
    return render_template("search_page.html", form=form, data=data)


if __name__ == "__main__":
    ui_app.run(debug=True, threaded=True)
