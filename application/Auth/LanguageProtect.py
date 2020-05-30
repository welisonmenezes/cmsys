from .Bases.BasicProtectionBase import *

class LanguageProtect(BasicProtectionBase):
    def __init__(self, authenticator):
        super(LanguageProtect, self).__init__(authenticator, 'ApiBP.languagecontroller', 'configuration', True)