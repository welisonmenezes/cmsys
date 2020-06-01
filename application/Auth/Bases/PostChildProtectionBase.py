from flask import  request
from Models import Post

class PostChildProtectionBase():
    """Only logged user can accsses post, put or delete route of this resource.
        The user must have capability with type post to access this resource."""

    def __init__(self, authenticator, endpoint=None, capability_type=None, context=None):

        if authenticator and endpoint and str(request.endpoint) == endpoint and capability_type and context:
            
            if request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':

                passport = authenticator.get_authorized_passport()
                capabilities = passport['user'].role.capabilities

                # The user can only update your own post element or, to update other ones, the field only_themselves must be False.
                if request.method == 'POST' or request.method == 'PUT':
                    data = request.get_json()
                    if not 'post_id' in data:
                        return True
                    post_result = authenticator.session.query(Post.id, Post.user_id, Post.post_type_id).filter_by(id=data['post_id']).first()
                    if post_result:
                        owner_id = post_result[1]
                        authenticator.verify_capabilities(capabilities, capability_type, 'can_write', owner_id=owner_id, user_id=passport['user'].id, post_type_id=post_result[2])
                    else:
                        authenticator.verify_capabilities(capabilities, capability_type, 'can_write')

                # The user can only delete your own post element or, to delete other ones, the field only_themselves must be False.
                elif request.method == 'DELETE':
                    el_result = authenticator.session.query(getattr(context, 'post_id')).filter_by(id=request.view_args['id']).first()
                    if el_result and el_result[0]:
                        post_result = authenticator.session.query(Post.id, Post.user_id, Post.post_type_id).filter_by(id=el_result[0]).first()
                        if post_result:
                            owner_id = post_result[1]
                            authenticator.verify_capabilities(capabilities, capability_type, 'can_delete', owner_id=owner_id, user_id=passport['user'].id, post_type_id=post_result[2])
                        else:
                            authenticator.verify_capabilities(capabilities, capability_type, 'can_delete')
                    else:
                        authenticator.verify_capabilities(capabilities, capability_type, 'can_delete')