from .RepositoryBase import RepositoryBase
from Models import Term, TermSchema, Post, Language, Taxonomy
from Validators import TermValidator
from Utils import Paginate, FilterBuilder, Helper
from ErrorHandlers import BadRequestError

class TermRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Term."""

    def __init__(self, session):
        super().__init__(session)
        
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Term, args)
            fb.set_like_filters(['parent_id', 'taxonomy_id', 'language_id'])

            try:
                fb.set_and_or_filter('s', 'or', [{'field':'name', 'type':'like'}, {'field':'display_name', 'type':'like'}, {'field':'description', 'type':'like'}])
            except Exception as e:
                raise BadRequestError(str(e))

            query = session.query(Term).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = TermSchema(many=True, exclude=self.get_exclude_fields(args, ['language', 'parent', 'children', 'taxonomy']))
            return self.handle_success(result, schema, 'get', 'Term')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = self.get_result_by_unique_key(id, Term, session)
            schema = TermSchema(many=False, exclude=self.get_exclude_fields(args, ['language', 'parent', 'children', 'taxonomy']))
            return self.handle_success(result, schema, 'get_by_id', 'Term')

        return self.response(run, False)


    def get_name_suggestions(self, name, args):
        """Returns names suggestions to new Media."""

        def run(session):
            return self.get_suggestions(name, Term, session)

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):
                term = Term()
                Helper().fill_object_from_data(term, data, ['name', 'display_name', 'description', 'parent_id', 'page_id', 'taxonomy_id', 'language_id'])
                self.add_foreign_keys(term, data, session, [('parent_id', Term), ('page_id', Post), ('language_id', Language), ('taxonomy_id', Taxonomy)])
                session.add(term)
                session.commit()
                return self.handle_success(None, None, 'create', 'Term', term.id)

            return self.validate_before(process, Helper().get_with_slug(request.get_json(), 'name'), TermValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                
                def fn(session, term):
                    Helper().fill_object_from_data(term, data, ['name', 'display_name', 'description', 'parent_id', 'page_id', 'taxonomy_id', 'language_id'])
                    self.add_foreign_keys(term, data, session, [('parent_id', Term), ('page_id', Post), ('language_id', Language), ('taxonomy_id', Taxonomy)])

                    if term.parent_id and int(term.parent_id) == int(id):
                        raise BadRequestError('The Term cannot be parent of yourself.')
                    
                    session.commit()
                    return self.handle_success(None, None, 'update', 'Term', term.id)

                return self.run_if_exists(fn, Term, id, session)

            return self.validate_before(process, Helper().get_with_slug(request.get_json(), 'name'), TermValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, term):
                if term.posts:
                    raise BadRequestError('You cannot delete this Term because it has a related Post.')
                self.set_children_as_null_to_delete(term, Term, session)
                session.delete(term)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Term', id)

            return self.run_if_exists(fn, Term, id, session)

        return self.response(run, True)


    def add_foreign_keys(self, current_context, data, session, configurations):
        """Controls if the list of foreign keys is an existing foreign key data. How to use:
            The configurtations must like: [('foreign_key_at_target_context, target_context)]"""

        for config in configurations:
            try:
                if config[0] == 'page_id':
                    """If the post referenced by the page_id is not post_type of type term-page, return error."""

                    el = self.get_existing_foreing_id(data, config[0], config[1], session, True)
                    if el and el.post_type and el.post_type.type != 'term-page':
                        raise BadRequestError('The Post_Type \'' + el.post_type.name + '\' of the parent post is \'' + el.post_type.type + '\' It must be \'term-page\'.')
                
                setattr(current_context, config[0], self.get_existing_foreing_id(data, config[0], config[1], session))

            except Exception as e:
                raise BadRequestError(str(e))