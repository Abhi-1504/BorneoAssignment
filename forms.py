"""
@author: Abhilash Raj

Module to create Search Form in UI
"""

from flask_wtf import FlaskForm  # For creating form
from wtforms import StringField, SubmitField  # Fields in form
from wtforms.validators import DataRequired  # Form validation


class SearchForm(FlaskForm):
    """Class to create search form for UI"""

    # Input Text Field with form validator of being non-empty
    search_field = StringField("Word/Phrase to search:", validators=[DataRequired()])

    # submit button for searching
    submit = SubmitField("Search")
