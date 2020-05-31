from .Bases.BasicProtectionBase import *

class TaxonomyProtect(BasicProtectionBase):
    def __init__(self, authenticator):
        super(TaxonomyProtect, self).__init__(authenticator, 'ApiBP.taxonomycontroller', 'taxonomy', True)