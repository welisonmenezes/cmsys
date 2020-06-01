from .Bases.OwnerProtectionBase import *
from Models import User

class UserProtect(OwnerProtectionBase):
    def __init__(self, authenticator):
        super(UserProtect, self).__init__(authenticator, 'ApiBP.usercontroller', 'user', User)