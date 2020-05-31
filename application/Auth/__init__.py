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
from .LanguageProtect import *
from .MediaProtect import *
from .MenuProtect import *
from .MenuItemProtect import *
from .NestProtect import *
from .PostProtect import *
from .PostTypeProtect import *
from .RoleProtect import *
from .SectorProtect import *
from .SocialProtect import *
from .TaxonomyProtect import *
from .TemplateProtect import *
from .TermProtect import *

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
    LanguageProtect(authenticator)
    MediaProtect(authenticator)
    MenuProtect(authenticator)
    MenuItemProtect(authenticator)
    NestProtect(authenticator)
    PostProtect(authenticator)
    PostTypeProtect(authenticator)
    RoleProtect(authenticator)
    SectorProtect(authenticator)
    SocialProtect(authenticator)
    TaxonomyProtect(authenticator)
    TemplateProtect(authenticator)
    TermProtect(authenticator)