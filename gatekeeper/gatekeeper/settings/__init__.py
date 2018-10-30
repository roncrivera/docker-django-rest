# Python
import os

# Django Split Settings
from split_settings.tools import optional, include

# Load default settings
from .defaults import *

ENV = os.environ.get('DJANGO_ENV') or 'playground'

include('{}.py'.format(ENV))
