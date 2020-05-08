from flask import make_response
from sqlalchemy import or_
import base64
from app import app_config
from .RepositoryBase import RepositoryBase
from Models import Media, MediaSchema, User
from Validators import MediaValidator
from Utils import Paginate, ErrorHandler, FilterBuilder, Helper

class MediaRepository(RepositoryBase):
    
    def get(self, args):
        def fn(session):
            fb = FilterBuilder(Media, args)
            fb.set_equals_filter('type')
            fb.set_equals_filter('origin')
            fb.set_equals_filter('user_id')

            try:
                fb.set_date_filter('created', date_modifier=args['date_modifier'])
                fb.set_between_dates_filter(
                    'created',
                    compare_date_time_one=args['compare_date_time_one'],
                    compare_date_time_two=args['compare_date_time_two'],
                    not_between=args['not_between']
                )
            except Exception as e:
                return ErrorHandler(400, str(e)).response

            filter = fb.get_filter()
            order_by = fb.get_order_by()
            page = fb.get_page()
            limit = fb.get_limit()

            if (args['s']):
                filter += (or_(Media.name.like('%'+args['s']+'%'), Meida.description.like('%'+args['s']+'%')),)

            query = session.query(Media).filter(*filter).order_by(*order_by)
            result = Paginate(query, page, limit)
            schema = MediaSchema(many=True)
            data = schema.dump(result.items)

            return {
                'data': data,
                'pagination': result.pagination
            }, 200

        return self.response(fn, False)
        

    def get_by_id(self, id, args):
        def fn(session):
            schema = MediaSchema(many=False)
            result = session.query(Media).filter_by(id=id).first()
            data = schema.dump(result)

            if (data):
                if (id and args['return_file_data'] == '1'):
                    data['file_base64'] = str(base64.b64encode(result.file[2:]))

                return {
                    'data': data
                }, 200
            else:
                return ErrorHandler(404, 'No Media found.').response

        return self.response(fn, False)


    def get_file(self, id):
        def fn(session):
            result = session.query(Media).filter_by(id=id).first()
            if (result):
                return self.file_response(result, False)
            else:
                return ErrorHandler(404, 'Culd not load this file.').response

        return self.response(fn, False)


    def get_image_preview(self, id):
        def fn(session):
            result = session.query(Media).filter_by(id=id).first()
            image_types = ['image/png', 'image/jpg', 'image/jpeg', 'image/gif', 'image/svg']
            if (result and result.type in image_types):
                return self.file_response(result, True)
            else:
                return self.image_not_found_response()

        return self.response(fn, False)


    def file_response(self, result, is_preview):
        saved_file = str(base64.b64encode(result.file))
        saved_file = saved_file[2:]
        imgdata = base64.b64decode(saved_file)
        file_ext = Helper.get_extension_by_type(result.type)
        response = make_response(imgdata)
        response.headers.set('Content-Type', result.type)
        if (not is_preview):
            response.headers.set('Content-Disposition', 'attachment; filename=' + result.name + '.' + file_ext)
        return response

    
    def image_not_found_response(self):

        notFoundImage = app_config['NOT_FOUND_IMAGE']
        imgdata = base64.b64decode(notFoundImage)
        response = make_response(imgdata)
        response.headers.set('Content-Type', 'image/png')
        return response
        
    
    def create(self, request):
        def fn(session):
            data = request.get_json()

            if (data):
                validator = MediaValidator(data)

                if (validator.is_valid()):

                    try:
                        file_details = self.get_file_details_from_request(data)
                    except Exception as e:
                        return ErrorHandler(400, e).response

                    media = Media(
                        name = data['name'],
                        description = data['description'],
                        type = file_details['type'],
                        file = file_details['data'],
                        origin = data['origin'],
                        user_id = data['user_id']
                    )
                    session.add(media)
                    session.commit()
                    last_id = media.id

                    return {
                        'message': 'Media saved successfully.',
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
                validator = MediaValidator(data)

                if (validator.is_valid(id=id)):

                    media = session.query(Media).filter_by(id=id).first()

                    if (Media):
                        media.name = data['name']
                        media.description = data['description']
                        media.origin = data['origin']
                        media.user_id = data['user_id']

                        if (data['file'] and data['file'] != ''):
                            try:
                                file_details = self.get_file_details_from_request(data)
                            except Exception as e:
                                return ErrorHandler(400, e).response

                            media.type = file_details['type']
                            media.file = file_details['data']

                        session.commit()

                        return {
                            'message': 'Media updated successfully.',
                            'id': media.id
                        }, 200
                    else:
                        return ErrorHandler(404, 'No Media found.').response

                else:
                    return ErrorHandler(400, validator.get_errors()).response

            else:
                return ErrorHandler(400, 'No data send.').response

        return self.response(fn, True)


    def get_file_details_from_request(self, data):
        try:
            type_and_data = Helper.get_file_type_and_data(data['file'])
            file_details = {
                'type': type_and_data[0],
                'data': base64.b64decode(type_and_data[1])
            }
            return file_details
        except:
            raise Exception('Cannot get file details. Please, check if it is a valid file.')


    def delete(self, id):
        def fn(session):
            media = session.query(Media).filter_by(id=id).first()

            if (media):

                # TODO: check if media can be deleted (if any post is related to the media, it cannot be deleted)

                user = session.query(User.id).filter_by(avatar_id=media.id).first()
                if (user):
                    return ErrorHandler(406, 'You cannot delete this File because it may have a related User.').response

                session.delete(media)
                session.commit()

                return {
                    'message': 'Media deleted successfully.',
                    'id': id
                }, 200
            else:
                return ErrorHandler(404, 'No Media found.').response

        return self.response(fn, True)