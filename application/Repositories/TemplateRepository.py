from .RepositoryBase import RepositoryBase
from Models import Template, TemplateSchema, PostType
from Validators import TemplateValidator
from Utils import Paginate, FilterBuilder, Helper
from ErrorHandlers import BadRequestError

class TemplateRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Template."""

    def __init__(self, session):
        super().__init__(session)
        
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        fb = FilterBuilder(Template, args)
        
        try:
            fb.set_and_or_filter('s', 'or', [{'field':'name', 'type':'like'}, {'field':'description', 'type':'like'}])
        except Exception as e:
            raise BadRequestError(str(e))

        query = self.session.query(Template).filter(*fb.get_filter()).order_by(*fb.get_order_by())
        result = Paginate(query, fb.get_page(), fb.get_limit())
        schema = TemplateSchema(many=True, exclude=self.get_exclude_fields(args, ['post_types']))
        return self.handle_success(result, schema, 'get', 'Template')
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        result = self.session.query(Template).filter_by(id=id).first()
        schema = TemplateSchema(many=False, exclude=self.get_exclude_fields(args, ['post_types']))
        return self.handle_success(result, schema, 'get_by_id', 'Template')

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def process(session, data):
            template = Template()
            Helper().fill_object_from_data(template, data, ['name', 'description', 'value'])
            session.add(template)
            session.commit()
            return self.handle_success(None, None, 'create', 'Template', template.id)

        return self.validate_before(process, request.get_json(), TemplateValidator, self.session)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def process(session, data):

            def fn(session, template):
                Helper().fill_object_from_data(template, data, ['name', 'description', 'value'])
                session.commit()
                return self.handle_success(None, None, 'update', 'Template', template.id)

            return self.run_if_exists(fn, Template, id, session)

        return self.validate_before(process, request.get_json(), TemplateValidator, self.session, id=id)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def fn(session, template):
            self.is_foreigners([(template, 'template_id', PostType)], session)
            session.delete(template)
            session.commit()
            return self.handle_success(None, None, 'delete', 'Template', id)

        return self.run_if_exists(fn, Template, id, self.session)