from .Bases.BasicProtectionBase import *

class TemplateProtect(BasicProtectionBase):
    def __init__(self, authenticator):
        super(TemplateProtect, self).__init__(authenticator, 'ApiBP.templatecontroller', 'post-type', False)