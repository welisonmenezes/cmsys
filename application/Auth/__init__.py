from .AuthUtils import *
from .BlacklistProtect import *
from .CapabilityProtect import *
from .CommentProtect import *
from .ConfigurationProtect import *

def protect_endpoints():
    """Run all endpoint protectors."""

    BlacklistProtect()
    CapabilityProtect()
    CommentProtect()
    ConfigurationProtect()