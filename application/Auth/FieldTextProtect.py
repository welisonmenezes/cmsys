from .Bases.PostChildProtectionBase import *
from Models import FieldText

class FieldTextProtect(PostChildProtectionBase):
    def __init__(self, authenticator):
        super(FieldTextProtect, self).__init__(authenticator, 'ApiBP.fieldtextcontroller', 'post', FieldText)