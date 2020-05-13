from .RepositoryBase import RepositoryBase
from Models import Template, TemplateSchema
from Validators import TemplateValidator
from Utils import Paginate, ErrorHandler, FilterBuilder

class TemplateRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Template."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Template, args)
            # fb.set_equals_filter('type')
            # fb.set_equals_filter('target')
            # fb.set_like_filter('value')

            query = session.query(Template).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = TemplateSchema(many=True)

            return {
                'data': schema.dump(result.items),
                'pagination': result.pagination
            }, 200

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Template).filter_by(id=id).first()
            schema = TemplateSchema(many=False)
            data = schema.dump(result)

            return {
                'data': schema.dump(result)
            }, 200

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):

                template = Template(
                    name = data['name'],
                    description = data['description'],
                    value = data['value']
                )
                session.add(template)
                session.commit()
                last_id = template.id

                return {
                    'message': 'Template saved successfully.',
                    'id': last_id
                }, 200

            return self.validate_before(process, request.get_json(), TemplateValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                template = session.query(Template).filter_by(id=id).first()

                if (template):
                    template.name = data['name']
                    template.description = data['description']
                    template.value = data['value']
                    session.commit()

                    return {
                        'message': 'Template updated successfully.',
                        'id': template.id
                    }, 200

                else:
                    return ErrorHandler().get_error(404, 'No Template found.')

            return self.validate_before(process, request.get_json(), TemplateValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):
            template = session.query(Template).filter_by(id=id).first()

            if (template):
                session.delete(template)
                session.commit()

                return {
                    'message': 'Template deleted successfully.',
                    'id': id
                }, 200
            else:
                return ErrorHandler().get_error(404, 'No Template found.')

        return self.response(run, True)