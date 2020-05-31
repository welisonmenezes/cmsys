from .Bases.BasicProtectionBase import *

class SectorProtect(BasicProtectionBase):
    def __init__(self, authenticator):
        super(SectorProtect, self).__init__(authenticator, 'ApiBP.sectorcontroller', 'menu', True)