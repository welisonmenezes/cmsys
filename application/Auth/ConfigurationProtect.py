from .BasicProtectionBase import *

class ConfigurationProtect(BasicProtectionBase):
    def __init__(self, authenticator):
        super(ConfigurationProtect, self).__init__(authenticator, 'ApiBP.configurationcontroller', 'configuration')