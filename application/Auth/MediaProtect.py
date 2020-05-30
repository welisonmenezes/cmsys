from .Bases.OwnerProtectionBase import *
from Models import Media

class MediaProtect(OwnerProtectionBase):
    def __init__(self, authenticator):
        super(MediaProtect, self).__init__(authenticator, 'ApiBP.mediacontroller', 'media', Media)