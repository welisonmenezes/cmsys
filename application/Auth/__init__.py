from .AuthUtils import *
from .BlacklistProtect import *
from .CapabilityProtect import *

def protect_endpoints():
    """Run all endpoint protectors."""

    BlacklistProtect()
    CapabilityProtect()