"""
This script is used for importing App package into our test suite.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import App
from App import app
from App import db
from App.models import LicenceModel
from App.tools import NameToLicence
from App.tools import IncorrectDateFormat