from .RepositoryBase import RepositoryBase
from Models import FieldFile, FieldFileSchema, Field, Media, Post, Grouper
from Validators import FieldFileValidator
from Utils import Paginate, ErrorHandler, FilterBuilder

class FieldFileRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of FieldFile."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(FieldFile, args)
            fb.set_equals_filters(['field_id', 'media_id', 'grouper_id', 'post_id'])

            query = session.query(FieldFile).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = FieldFileSchema(many=True)
            return self.handle_success(result, schema, 'get', 'FieldFile')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(FieldFile).filter_by(id=id).first()
            schema = FieldFileSchema(many=False)
            return self.handle_success(result, schema, 'get_by_id', 'FieldFile')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):

                field_file = FieldFile()

                can_add_ref = self.forbid_save_with_different_parent_reference(data, session, [('field_id', 'grouper_id', Field), ('field_id', 'post_id', Field)])
                if can_add_ref != True:
                    return can_add_ref

                fk_was_added = self.add_foreign_keys(field_file, data, session, [('field_id', Field), ('media_id', Media), ('grouper_id', Grouper), ('post_id', Post)])
                if fk_was_added != True:
                    return fk_was_added

                session.add(field_file)
                session.commit()
                return self.handle_success(None, None, 'create', 'FieldFile', field_file.id)

            return self.validate_before(process, request.get_json(), FieldFileValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                
                def fn(session, field_file):

                    can_add_ref = self.forbid_save_with_different_parent_reference(data, session, [('field_id', 'grouper_id', Field), ('field_id', 'post_id', Field)])
                    if can_add_ref != True:
                        return can_add_ref

                    fk_was_added = self.add_foreign_keys(field_file, data, session, [('field_id', Field), ('media_id', Media), ('grouper_id', Grouper), ('post_id', Post)])
                    if fk_was_added != True:
                        return fk_was_added
                        
                    session.commit()
                    return self.handle_success(None, None, 'update', 'FieldFile', field_file.id)

                return self.run_if_exists(fn, FieldFile, id, session)

            return self.validate_before(process, request.get_json(), FieldFileValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, field_file):
                session.delete(field_file)
                session.commit()
                return self.handle_success(None, None, 'delete', 'FieldFile', id)

            return self.run_if_exists(fn, FieldFile, id, session)

        return self.response(run, True)