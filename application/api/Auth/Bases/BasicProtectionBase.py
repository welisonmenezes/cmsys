from flask import  request

class BasicProtectionBase():
    """Only logged user can accsses any route of this resource.
        The user must have capability with type configuration to access this resource."""

    def __init__(self, authenticator=None, endpoint=None, capability_type=None, is_get_public=False):

        if authenticator and endpoint and str(request.endpoint) == endpoint and capability_type:
                
            # To read can_read must be True
            if request.method == 'GET' and not is_get_public:

                passport = authenticator.get_authorized_passport()
                capabilities = passport['user'].role.capabilities
                authenticator.verify_capabilities(capabilities, capability_type, 'can_read')


            if request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':

                passport = authenticator.get_authorized_passport()
                capabilities = passport['user'].role.capabilities

                # To write can_write must be True
                if request.method == 'POST' or request.method == 'PUT':
                    authenticator.verify_capabilities(capabilities, capability_type, 'can_write')

                # To delete can_delete must be True
                elif request.method == 'DELETE':
                    authenticator.verify_capabilities(capabilities, capability_type, 'can_delete')