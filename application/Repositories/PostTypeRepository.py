from .RepositoryBase import RepositoryBase
from Models import PostType, PostTypeSchema
from Validators import PostTypeValidator
from Utils import Paginate, ErrorHandler, FilterBuilder

class PostTypeRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of PostType."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(PostType, args)
            # fb.set_equals_filter('type')
            # fb.set_equals_filter('target')
            # fb.set_like_filter('value')

            query = session.query(PostType).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = PostTypeSchema(many=True)

            return {
                'data': schema.dump(result.items),
                'pagination': result.pagination
            }, 200

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(PostType).filter_by(id=id).first()
            schema = PostTypeSchema(many=False)
            data = schema.dump(result)

            return {
                'data': schema.dump(result)
            }, 200

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):

                post_type = PostType(
                    name = data['name'],
                    type = data['type'],
                    template_id = data['template_id']
                )
                session.add(post_type)
                session.commit()
                last_id = post_type.id

                return {
                    'message': 'PostType saved successfully.',
                    'id': last_id
                }, 200

            return self.validate_before(process, request.get_json(), PostTypeValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                post_type = session.query(PostType).filter_by(id=id).first()

                if (post_type):
                    post_type.name = data['name']
                    post_type.type = data['type']
                    post_type.template_id = data['template_id']
                    session.commit()

                    return {
                        'message': 'PostType updated successfully.',
                        'id': post_type.id
                    }, 200

                else:
                    return ErrorHandler().get_error(404, 'No PostType found.')

            return self.validate_before(process, request.get_json(), PostTypeValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):
            post_type = session.query(PostType).filter_by(id=id).first()

            if (post_type):
                session.delete(post_type)
                session.commit()

                return {
                    'message': 'PostType deleted successfully.',
                    'id': id
                }, 200
            else:
                return ErrorHandler().get_error(404, 'No PostType found.')

        return self.response(run, True)