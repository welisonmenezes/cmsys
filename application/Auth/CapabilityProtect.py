from flask import  request

class CapabilityProtect():
    """Only logged user can accsses any route of this resource.
        The user must have capability with type capability to access this resource."""

    def __init__(self, authenticator):

        if str(request.endpoint) == 'ApiBP.capabilitycontroller':

            passport = authenticator.get_authorized_passport()
            capabilities = passport['user'].role.capabilities

            # To read can_read must be True
            if request.method == 'GET':
                authenticator.verify_capabilities(capabilities, 'capability', 'can_read')

            # To write can_write must be True
            elif request.method == 'POST' or request.method == 'PUT':
                authenticator.verify_capabilities(capabilities, 'capability', 'can_write')

            # To delete can_delete must be True
            elif request.method == 'DELETE':
                authenticator.verify_capabilities(capabilities, 'capability', 'can_delete')