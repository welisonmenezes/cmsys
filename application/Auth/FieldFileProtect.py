from .Bases.PostChildProtectionBase import *
from Models import FieldFile

class FieldFileProtect(PostChildProtectionBase):
    def __init__(self, authenticator):
        super(FieldFileProtect, self).__init__(authenticator, 'ApiBP.fieldfilecontroller', 'post', FieldFile)