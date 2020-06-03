from .Bases.BasicProtectionBase import *

class MenuProtect(BasicProtectionBase):
    def __init__(self, authenticator):
        super(MenuProtect, self).__init__(authenticator, 'ApiBP.menucontroller', 'menu', True)