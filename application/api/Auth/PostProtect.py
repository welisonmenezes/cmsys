from .Bases.OwnerProtectionBase import *
from Models import Post

class PostProtect(OwnerProtectionBase):
    def __init__(self, authenticator):
        super(PostProtect, self).__init__(authenticator, 'ApiBP.postcontroller', 'post', Post)