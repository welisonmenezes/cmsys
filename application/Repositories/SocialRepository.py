from .RepositoryBase import RepositoryBase
from Models import Social, SocialSchema
from Validators import SocialValidator
from Utils import Paginate, ErrorHandler, Checker, FilterBuilder

class SocialRepository(RepositoryBase):

    def set_query_fields(self, args):
        self.fields = [
            Social.id,
            Social.name,
            Social.url,
            Social.target,
            Social.description,
            Social.origin,
            Social.configuration_id,
            Social.user_id
        ]

    
    def get(self, args):
        def fn(session):
            fb = FilterBuilder(Social, args)
            fb.set_like_filter('name')
            fb.set_equals_filter('origin')
            fb.set_equals_filter('user_id')
            filter = fb.get_filter()
            order_by = fb.get_order_by()
            page = fb.get_page()
            limit = fb.get_limit()

            self.set_query_fields(args)

            query = session.query(*self.fields).filter(*filter).order_by(*order_by)
            result = Paginate(query, page, limit)
            schema = SocialSchema(many=True)
            data = schema.dump(result.items)

            return {
                'data': data,
                'pagination': result.pagination
            }, 200

        return self.response(fn, False)
        

    def get_by_id(self, id):
        def fn(session):
            self.set_query_fields(args)

            schema = SocialSchema(many=False)
            result = session.query(*self.fields).filter_by(id=id).first()
            data = schema.dump(result)

            if (data):
                return {
                    'data': data
                }, 200
            else:
                return ErrorHandler(404, 'No Social found.').response

        return self.response(fn, False)

    
    def create(self, request):
        def fn(session):
            data = request.get_json()

            if (data):
                validator = SocialValidator(data)

                if (validator.is_valid()):
                    social = Social(
                        name = data['name'],
                        url = data['url'],
                        target = data['target'],
                        description = data['description'],
                        origin = data['origin'],
                        #configuration_id = data['configuration_id'],
                        #user_id = data['user_id']
                    )

                    # TODO: implement validations to add a valid configuration (check origin)
                    # TODO: implement validations to add a valid user (check origin)

                    session.add(social)
                    session.commit()
                    last_id = social.id

                    return {
                        'message': 'Social saved successfully.',
                        'id': last_id
                    }, 200
                else:
                    return ErrorHandler(400, validator.get_errors()).response

            else:
                return ErrorHandler(400, 'No data send.').response

        return self.response(fn, True)


    def update(self, id, request):
        def fn(session):
            data = request.get_json()

            if (data):
                validator = SocialValidator(data)

                if (validator.is_valid(id=id)):
                    social = session.query(Social).filter_by(id=id).first()

                    if (social):
                        social.name = data['name']
                        social.url = data['url']
                        social.target = data['target']
                        social.origin = data['origin']
                        social.description = data['description']
                        #social.configuration_id = data['configuration_id']
                        #social.user_id = data['user_id']

                        # TODO: implement validations to edit configuration (check origin)
                        # TODO: implement validations to edit user (check origin)

                        session.commit()

                        return {
                            'message': 'Social updated successfully.',
                            'id': social.id
                        }, 200
                    else:
                        return ErrorHandler(404, 'No Social found.').response

                else:
                    return ErrorHandler(400, validator.get_errors()).response

            else:
                return ErrorHandler(400, 'No data send.').response

        return self.response(fn, True)


    def delete(self, id):
        def fn(session):
            social = session.query(Social).filter_by(id=id).first()

            if (social):
                session.delete(social)
                session.commit()

                return {
                    'message': 'Social deleted successfully.',
                    'id': id
                }, 200
            else:
                return ErrorHandler(404, 'No Social found.').response

        return self.response(fn, True)