from .Bases.BasicProtectionBase import *

class CapabilityProtect(BasicProtectionBase):
    def __init__(self, authenticator):
        super(CapabilityProtect, self).__init__(authenticator, 'ApiBP.capabilitycontroller', 'capability')