import sys
import os
from os.path import join, dirname, abspath

# Add the project directory to the sys.path
sys.path.insert(0, abspath(join(dirname(__file__), 'aiwebproject2')))

# Ensure the Python working directory is set to public_html
sys.path.insert(1, '/home/u036/public_html/brainbite/aiwebproject2')

# Change the current working directory to the application's directory
os.chdir('/home/u036/public_html/brainbite/aiwebproject2')

# Activate the virtual environment
activate_this = join(dirname(__file__), '../venv/bin/activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import the Flask application
from app import app
application = app

# Error handler for internal server errors
import traceback
@app.errorhandler(500)
def internal_error(exception):
    return "<pre>" + traceback.format_exc() + "</pre>"