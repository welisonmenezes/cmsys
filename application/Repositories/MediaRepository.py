from flask import make_response
import base64
from app import app
from .RepositoryBase import RepositoryBase
from Models import Media, MediaSchema, User, FieldFile
from Validators import MediaValidator
from Utils import Paginate, FilterBuilder, Helper
from ErrorHandlers import BadRequestError, NotFoundError

class MediaRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Media."""

    def __init__(self, session):
        super().__init__(session)
        
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        fb = FilterBuilder(Media, args)
        fb.set_equals_filters(['type', 'origin', 'user_id'])

        try:
            fb.set_date_filter('created', date_modifier=args['date_modifier'])
            fb.set_between_dates_filter(
                'created', not_between=args['not_between'],
                compare_date_time_one=args['compare_date_time_one'],
                compare_date_time_two=args['compare_date_time_two']
            )
            fb.set_and_or_filter('s', 'or', [{'field':'name', 'type':'like'}, {'field':'description', 'type':'like'}])
        except Exception as e:
            raise BadRequestError(str(e))

        query = self.session.query(Media).filter(*fb.get_filter()).order_by(*fb.get_order_by())
        result = Paginate(query, fb.get_page(), fb.get_limit())
        schema = MediaSchema(many=True, exclude=self.get_exclude_fields(args, ['user']))
        return self.handle_success(result, schema, 'get', 'Media')
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        result = self.get_result_by_unique_key(id, Media, self.session)
        schema = MediaSchema(many=False, exclude=self.get_exclude_fields(args, ['user']))
        data = schema.dump(result)

        if (data):
            if (id and args['return_file_data'] == '1'):
                data['file_base64'] = str(base64.b64encode(result.file[2:]))

            return {
                'data': data
            }, 200
            
        else:
            raise NotFoundError('No Media found.')


    def get_name_suggestions(self, name, args):
        """Returns names suggestions to new Media."""

        return self.get_suggestions(name, Media, self.session)


    def get_file(self, id, args):
        """Returns the file to donwload (run when download_file == 1 configured at controller)."""

        result = self.get_result_by_unique_key(id, Media, self.session)
        if (result):
            return self.file_response(result, False)
        else:
            raise NotFoundError('Could not load this file.')


    def get_image_preview(self, id):
        """Returns the image preview
            (This method is called by the Image Controller which has its own endpoint for this purpose)."""

        result = self.get_result_by_unique_key(id, Media, self.session)
        image_types = ['image/png', 'image/jpg', 'image/jpeg', 'image/gif', 'image/svg']
        if (result and result.type in image_types):
            return self.file_response(result, True)
        else:
            return self.image_not_found_response()

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def process(session, data):
            
            try:
                file_details = Helper().get_file_details_from_request(data)
            except Exception as e:
                raise BadRequestError(str(e))

            media = Media(
                type = file_details['type'],
                file = file_details['data'],
                created = Helper().get_current_datetime()
            )
            Helper().fill_object_from_data(media, data, ['name', 'description', 'extension', 'origin'])
            self.add_foreign_keys(media, data, session, [('user_id', User)])
            session.add(media)
            session.commit()
            return self.handle_success(None, None, 'create', 'Media', media.id)

        return self.validate_before(process, Helper().get_with_slug(request.get_json(), 'name'), MediaValidator, self.session)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def process(session, data):

            def fn(session, media):
                Helper().fill_object_from_data(media, data, ['name', 'description', 'extension', 'origin'])
                self.add_foreign_keys(media, data, session, [('user_id', User)])

                if 'file' in data and data['file'] != '':

                    try:
                        file_details = Helper().get_file_details_from_request(data)
                    except Exception as e:
                        raise BadRequestError(str(e))

                    media.type = file_details['type']
                    media.file = file_details['data']

                session.commit()
                return self.handle_success(None, None, 'update', 'Media', media.id)

            return self.run_if_exists(fn, Media, id, session)

        return self.validate_before(process, Helper().get_with_slug(request.get_json(), 'name'), MediaValidator, self.session, id=id)

    
    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def fn(session, media):
            self.is_foreigners([(media, 'avatar_id', User), (media, 'media_id', FieldFile)], session)
            session.delete(media)
            session.commit()
            return self.handle_success(None, None, 'delete', 'Media', id)

        return self.run_if_exists(fn, Media, id, self.session)


    def file_response(self, result, is_preview):
        """Returns the file, or to preview or to download."""

        saved_file = str(base64.b64encode(result.file))
        saved_file = saved_file[2:]
        imgdata = base64.b64decode(saved_file)
        response = make_response(imgdata)
        response.headers.set('Content-Type', result.type)
        if (not is_preview):
            response.headers.set('Content-Disposition', 'attachment; filename=' + result.name + '.' + result.extension)
        return response

    
    def image_not_found_response(self):
        """Provides a default image preview if the requested image preview was fail."""

        notFoundImage = app.config['NOT_FOUND_IMAGE']
        imgdata = base64.b64decode(notFoundImage)
        response = make_response(imgdata)
        response.headers.set('Content-Type', 'image/png')
        return response