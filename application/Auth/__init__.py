from .AuthUtils import *
from .BlacklistProtect import *
from .CapabilityProtect import *
from .CommentProtect import *
from .ConfigurationProtect import *
from .FieldProtect import *
from .FieldContentProtect import *
from .FieldFileProtect import *
from .FieldTextProtect import *
from .GrouperProtect import *
from .NestProtect import *
from .PostProtect import *

def protect_endpoints():
    """Run all endpoint protectors."""

    authenticator = AuthUtils()
    BlacklistProtect(authenticator)
    CapabilityProtect(authenticator)
    CommentProtect(authenticator)
    ConfigurationProtect(authenticator)
    FieldProtect(authenticator)
    FieldContentProtect(authenticator)
    FieldFileProtect(authenticator)
    FieldTextProtect(authenticator)
    GrouperProtect(authenticator)
    NestProtect(authenticator)
    PostProtect(authenticator)