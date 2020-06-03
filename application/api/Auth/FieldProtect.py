from .Bases.PostChildProtectionBase import *
from Models import Field

class FieldProtect(PostChildProtectionBase):
    def __init__(self, authenticator):
        super(FieldProtect, self).__init__(authenticator, 'ApiBP.fieldcontroller', 'post', Field)