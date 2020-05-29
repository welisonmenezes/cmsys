from flask import  request
from Models import Post

class PostProtect():
    """Only logged user can accsses post, put and delete endpoints of this resource."""

    def __init__(self, authenticator):

        if str(request.endpoint) == 'ApiBP.postcontroller':

            if request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':

                passport = authenticator.get_authorized_passport()
                capabilities = passport['user'].role.capabilities
                data = request.get_json()

                # The user can only post your own Post
                if request.method == 'POST':
                    if data['user_id'] != passport['user'].id:
                        authenticator.verify_capabilities(capabilities, 'post', 'can_write')

                # The user can only update your own Post or, to update others Post, the field only_themselves must be False.
                # If the field only_themselves is False the user cannot change the user_id field.
                if  request.method == 'PUT':
                    owner_result = authenticator.session.query(Post.user_id).filter_by(id=request.view_args['id']).first()
                    if owner_result:
                        owner_id = owner_result[0]
                        authenticator.verify_capabilities(capabilities, 'post', 'can_write', owner_id=owner_id, user_id=passport['user'].id, new_owner_id=data['user_id'])

                # The user can only delete your own Post, or to delete others Post the field only_themselves must be False
                elif request.method == 'DELETE':
                    owner_result = authenticator.session.query(Post.user_id).filter_by(id=request.view_args['id']).first()
                    if owner_result:
                        owner_id = owner_result[0]
                        authenticator.verify_capabilities(capabilities, 'post', 'can_delete', owner_id=owner_id, user_id=passport['user'].id)