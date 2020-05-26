from .AuthUtils import *
from .BlacklistProtect import *

def protect_endpoints():
    """Run all endpoint protectors."""

    BlacklistProtect()