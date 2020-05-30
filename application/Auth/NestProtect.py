from .Bases.PostChildProtectionBase import *
from Models import Nest

class NestProtect(PostChildProtectionBase):
    def __init__(self, authenticator):
        super(NestProtect, self).__init__(authenticator, 'ApiBP.nestcontroller', 'post', Nest)