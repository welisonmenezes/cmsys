from flask import  request
from Models import Comment

class CommentProtect():
    """Only logged user can accsses post, put and delete endpoints of this resource."""

    def __init__(self, authenticator):

        if str(request.endpoint) == 'ApiBP.commentcontroller':

            if request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':

                passport = authenticator.get_authorized_passport()
                capabilities = passport['user'].role.capabilities
                data = request.get_json()

                # The user can only post your own comment
                if request.method == 'POST':
                    if data['user_id'] != passport['user'].id:
                        authenticator.verify_capabilities(capabilities, 'comment', 'can_write')

                # The user can only update your own comment or, to update others comment, the field only_themselves must be False.
                # If the field only_themselves is False the user cannot change the user_id field.
                if  request.method == 'PUT':
                    owner_result = authenticator.session.query(Comment.user_id).filter_by(id=request.view_args['id']).first()
                    if owner_result:
                        owner_id = owner_result[0]
                        authenticator.verify_capabilities(capabilities, 'comment', 'can_write', owner_id=owner_id, user_id=passport['user'].id, new_owner_id=data['user_id'])

                # The user can only delete your own comment, or to delete others comment the field only_themselves must be False
                elif request.method == 'DELETE':
                    owner_result = authenticator.session.query(Comment.user_id).filter_by(id=request.view_args['id']).first()
                    if owner_result:
                        owner_id = owner_result[0]
                        authenticator.verify_capabilities(capabilities, 'comment', 'can_delete', owner_id=owner_id, user_id=passport['user'].id)