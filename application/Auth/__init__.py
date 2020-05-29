from .AuthUtils import *
from .BlacklistProtect import *
from .CapabilityProtect import *
from .CommentProtect import *
from .ConfigurationProtect import *
from .FieldProtect import *

def protect_endpoints():
    """Run all endpoint protectors."""

    authenticator = AuthUtils()
    BlacklistProtect(authenticator)
    CapabilityProtect(authenticator)
    CommentProtect(authenticator)
    ConfigurationProtect(authenticator)
    FieldProtect(authenticator)