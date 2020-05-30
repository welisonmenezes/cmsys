from .Bases.PostChildProtectionBase import *
from Models import Grouper

class GrouperProtect(PostChildProtectionBase):
    def __init__(self, authenticator):
        super(GrouperProtect, self).__init__(authenticator, 'ApiBP.groupercontroller', 'post', Grouper)