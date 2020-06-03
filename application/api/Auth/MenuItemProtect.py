from .Bases.BasicProtectionBase import *

class MenuItemProtect(BasicProtectionBase):
    def __init__(self, authenticator):
        super(MenuItemProtect, self).__init__(authenticator, 'ApiBP.menuitemcontroller', 'menu', True)