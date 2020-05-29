from flask import  request
from Models import Post, Field, FieldContent, FieldFile, FieldText, Nest, Grouper

class FieldProtect():
    """Only logged user can accsses post, put or delete route of this resource.
        The user must have capability with type post to access this resource."""

    def __init__(self, authenticator):

        if str(request.endpoint) == 'ApiBP.fieldcontroller' or str(request.endpoint) == 'ApiBP.fieldcontentcontroller' or \
        str(request.endpoint) == 'ApiBP.fieldfilecontroller' or str(request.endpoint) == 'ApiBP.fieldtextcontroller' or \
        str(request.endpoint) == 'ApiBP.nestcontroller' or str(request.endpoint) == 'ApiBP.groupercontroller':

            # TODO: see how implement the private post request

            if request.method == 'GET':
                pass
            
            if request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':

                passport = authenticator.get_authorized_passport()
                capabilities = passport['user'].role.capabilities

                # The user can only update your own post element or, to update other ones, the field only_themselves must be False.
                if request.method == 'POST' or request.method == 'PUT':
                    data = request.get_json()
                    post_result = authenticator.session.query(Post.id, Post.user_id).filter_by(id=data['post_id']).first()
                    if post_result:
                        owner_id = post_result[1]
                        authenticator.verify_capabilities(capabilities, 'post', 'can_write', owner_id=owner_id, user_id=passport['user'].id)
                    else:
                        authenticator.verify_capabilities(capabilities, 'post', 'can_write')

                # The user can only delete your own post element or, to delete other ones, the field only_themselves must be False.
                elif request.method == 'DELETE':
                    context = None
                    if str(request.endpoint) == 'ApiBP.fieldcontroller':
                        context = Field
                    elif str(request.endpoint) == 'ApiBP.fieldcontentcontroller':
                        context = FieldContent
                    elif str(request.endpoint) == 'ApiBP.fieldfilecontroller':
                        context = FieldFile
                    elif str(request.endpoint) == 'ApiBP.fieldtextcontroller':
                        context = FieldText
                    elif str(request.endpoint) == 'ApiBP.nestcontroller':
                        context = Nest
                    elif str(request.endpoint) == 'ApiBP.groupercontroller':
                        context = Grouper
                    el_result = authenticator.session.query(getattr(context, 'post_id')).filter_by(id=request.view_args['id']).first()
                    if el_result and el_result[0]:
                        post_result = authenticator.session.query(Post.id, Post.user_id).filter_by(id=el_result[0]).first()
                        if post_result:
                            owner_id = post_result[1]
                            authenticator.verify_capabilities(capabilities, 'post', 'can_delete', owner_id=owner_id, user_id=passport['user'].id)
                        else:
                            authenticator.verify_capabilities(capabilities, 'post', 'can_delete')
                    else:
                        authenticator.verify_capabilities(capabilities, 'post', 'can_delete')