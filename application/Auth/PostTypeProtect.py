from .Bases.BasicProtectionBase import *

class PostTypeProtect(BasicProtectionBase):
    def __init__(self, authenticator):
        super(PostTypeProtect, self).__init__(authenticator, 'ApiBP.posttypecontroller', 'post-type', False)