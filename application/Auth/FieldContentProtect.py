from .Bases.PostChildProtectionBase import *
from Models import FieldContent

class FieldContentProtect(PostChildProtectionBase):
    def __init__(self, authenticator):
        super(FieldContentProtect, self).__init__(authenticator, 'ApiBP.fieldcontentcontroller', 'post', FieldContent)