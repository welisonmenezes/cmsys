from .Bases.BasicProtectionBase import *

class BlacklistProtect(BasicProtectionBase):
    def __init__(self, authenticator):
        super(BlacklistProtect, self).__init__(authenticator, 'ApiBP.blacklistcontroller', 'configuration')