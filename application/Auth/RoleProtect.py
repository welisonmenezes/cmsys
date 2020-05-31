from .Bases.BasicProtectionBase import *

class RoleProtect(BasicProtectionBase):
    def __init__(self, authenticator):
        super(RoleProtect, self).__init__(authenticator, 'ApiBP.rolecontroller', 'capability', False)