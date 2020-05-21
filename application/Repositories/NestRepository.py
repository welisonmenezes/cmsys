from .RepositoryBase import RepositoryBase
from Models import Nest, NestSchema, Post, PostType
from Validators import NestValidator
from Utils import Paginate, ErrorHandler, FilterBuilder

class NestRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Nest."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Nest, args)
            fb.set_equals_filters(['post_type_id', 'post_id'])
            
            try:
                fb.set_and_or_filter('s', 'or', [{'field':'name', 'type':'like'}, {'field':'description', 'type':'like'}])
            except Exception as e:
                return ErrorHandler().get_error(400, str(e))

            query = session.query(Nest).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = NestSchema(many=True, exclude=self.get_exclude_fields(args, ['post', 'post_type']))
            return self.handle_success(result, schema, 'get', 'Nest')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Nest).filter_by(id=id).first()
            schema = NestSchema(many=False, exclude=self.get_exclude_fields(args, ['post', 'post_type']))
            return self.handle_success(result, schema, 'get_by_id', 'Nest')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):
                nest = Nest(
                    name = data['name'],
                    description = data['description'],
                    limit = data['limit'],
                    has_pagination = data['has_pagination']
                )
                self.add_foreign_keys(nest, data, session, [('post_id', Post), ('post_type_id', PostType)])
                session.add(nest)
                session.commit()
                return self.handle_success(None, None, 'create', 'Nest', nest.id)

            return self.validate_before(process, request.get_json(), NestValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                
                def fn(session, nest):
                    nest.name = data['name']
                    nest.description = data['description']
                    nest.limit = data['limit']
                    nest.has_pagination = data['has_pagination']
                    self.add_foreign_keys(nest, data, session, [('post_id', Post), ('post_type_id', PostType)])
                    session.commit()
                    return self.handle_success(None, None, 'update', 'Nest', nest.id)

                return self.run_if_exists(fn, Nest, id, session)

            return self.validate_before(process, request.get_json(), NestValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, nest):
                session.delete(nest)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Nest', id)

            return self.run_if_exists(fn, Nest, id, session)

        return self.response(run, True)


    def add_foreign_keys(self, current_context, data, session, configurations):
        """Controls if the list of foreign keys is an existing foreign key data. How to use:
            The configurtations must like: [('foreign_key_at_target_context, target_context)]"""

        for config in configurations:
            try:
                if config[0] == 'post_type_id':
                    """If the post_type is not of type nested-page so return an error."""

                    el = self.get_existing_foreing_id(data, config[0], config[1], session, True)
                    if el and el.type != 'nested-page':
                        raise AttributeError('The Post_Type must have the type \'nested-page\'.')

                setattr(current_context, config[0], self.get_existing_foreing_id(data, config[0], config[1], session))
            except Exception as e:
                raise Exception(e)