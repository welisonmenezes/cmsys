from .Bases.OwnerProtectionBase import *
from Models import Comment

class CommentProtect(OwnerProtectionBase):
    def __init__(self, authenticator):
        super(CommentProtect, self).__init__(authenticator, 'ApiBP.commentcontroller', 'comment', Comment)