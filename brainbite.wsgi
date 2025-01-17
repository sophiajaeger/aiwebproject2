import sys
import os
from os.path import join, dirname, abspath



# Import the Flask application
from simple_app import app
application = app

# Error handler for internal server errors
import traceback
@app.errorhandler(500)
def internal_error(exception):
    return "<pre>" + traceback.format_exc() + "</pre>"