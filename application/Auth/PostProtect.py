from .Bases.OwnerProtectionBase import *
from Models import Post

# TODO: see how implement the private post request

class PostProtect(OwnerProtectionBase):
    def __init__(self, authenticator):
        super(PostProtect, self).__init__(authenticator, 'ApiBP.postcontroller', 'post', Post)