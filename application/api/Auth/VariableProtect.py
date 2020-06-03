from .Bases.BasicProtectionBase import *

class VariableProtect(BasicProtectionBase):
    def __init__(self, authenticator):
        super(VariableProtect, self).__init__(authenticator, 'ApiBP.variablecontroller', 'configuration', True)