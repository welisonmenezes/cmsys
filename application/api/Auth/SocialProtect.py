from .Bases.BasicProtectionBase import *

class SocialProtect(BasicProtectionBase):
    def __init__(self, authenticator):
        super(SocialProtect, self).__init__(authenticator, 'ApiBP.socialcontroller', 'configuration', True)