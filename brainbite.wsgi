import sys
import os
from os.path import join, dirname, abspath

# Add the project directory to the sys.path
sys.path.insert(0, abspath(join(dirname(__file__), 'aiwebproject2')))

# Activate the virtual environment
activate_this = join(dirname(__file__), 'venv/bin/activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app import app
application = app