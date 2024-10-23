
def _api_version():
    with open('VERSION', 'r') as fh_version:
        version = fh_version.read()
    return version

VERSION = _api_version()
