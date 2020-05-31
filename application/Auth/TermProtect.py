from .Bases.BasicProtectionBase import *

class TermProtect(BasicProtectionBase):
    def __init__(self, authenticator):
        super(TermProtect, self).__init__(authenticator, 'ApiBP.termcontroller', 'taxonomy', True)