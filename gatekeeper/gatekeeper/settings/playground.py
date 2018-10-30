# Playground settings for Gatekeeper project

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

# If any local_*.py files are present in gatekeeper/settings/, use them
# to override default settings for development.
try:
    include(optional('local_*.py'), scope=locals())
except ImportError:
    traceback.print_exc()
    sys.exit(1)
