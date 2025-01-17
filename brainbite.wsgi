import sys
import os
from os.path import join, dirname, abspath

# Add the project directory to the sys.path
sys.path.insert(0, abspath(join(dirname(__file__), '.')))

# Ensure the Python working directory is set to public_html
sys.path.insert(1, '/home/u036/public_html/aiwebproject2')

# Change the current working directory to the application's directory
os.chdir('/home/u036/public_html/aiwebproject2')

# Import the Flask application
from simple_app import app
application = app

# Error handler for internal server errors
import traceback
@app.errorhandler(500)
def internal_error(exception):
    return "<pre>" + traceback.format_exc() + "</pre>"