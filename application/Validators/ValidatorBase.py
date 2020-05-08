import base64
from Utils import Helper
from app import app_config

class ValidatorBase():

    def handle_validation_error(self, message):
        self.errors.append({ 'message': message })
        self.has_error = True


    def has_key(self, key, config):
        if ('key_required' in config and config['key_required']):
            if (not key in self.request):
                self.handle_validation_error('The request object does not have the field: \'' + key + '\'.')
                self.complete_key_list = False

    
    def is_empty_on_create(self, key, config, extra_args):
        if ('field_required_only_post' in config and config['field_required_only_post'] and key in self.request):
            if ('id' not in extra_args):
                if (not self.request[key] and self.request[key] == ''):
                    self.handle_validation_error('The field \'' + key + '\' cannot be empty.')

    
    def is_empty(self, key, config):
        if ('field_required' in config and config['field_required'] and key in self.request):
            if (not self.request[key] and self.request[key] == ''):
                self.handle_validation_error('The field \'' + key + '\' cannot be empty.')


    def max_length(self, key, config):
        if ('max_length' in config and isinstance(config['max_length'], int) and key in self.request):
            if (len(str(self.request[key])) > config['max_length']):
                self.handle_validation_error('The field \'' + key + '\' length cannot be greater than ' + str(config['max_length'] + '.'))


    def min_length(self, key, config):
        if ('min_length' in config and isinstance(config['min_length'], int) and key in self.request):
            if (len(str(self.request[key])) < config['min_length']):
                self.handle_validation_error('The field \'' + key + '\' length cannot be less than ' + str(config['min_length'] + '.'))


    def is_integer(self, key, config):
        if ('is_integer' in config and isinstance(config['is_integer'], int) and key in self.request):
            if (not isinstance(self.request[key], int)):
                self.handle_validation_error('The field \'' + key + '\' must be an integer.')

    
    def is_boolean(self, key, config):
        if ('is_boolean' in config and isinstance(config['is_boolean'], int) and key in self.request):
            if (not isinstance(self.request[key], int) or self.request[key] < 0 or self.request[key] > 1):
                self.handle_validation_error('The field \'' + key + '\' only accpet 0 or 1 value.')


    def is_unique(self, key, config, extra_args):
        if ('is_unique' in config and isinstance(config['is_unique'], int) and key in self.request):
            el = self.session.query(self.model).filter(getattr(self.model, key)==self.request[key]).first()
            if (el):
                if ('id' in extra_args):
                    if (getattr(el, key) == self.request[key]):
                        if (extra_args['id'] != el.id):
                            self.handle_validation_error('The field \'' + key + '\' already exists in database.')
                else:        
                    self.handle_validation_error('The field \'' + key + '\' already exists in database.')

    
    def is_file(self, key, config):
        if ('is_file' in config and key in self.request and self.request[key] != ''):
            try:
                type_and_data = Helper.get_file_type_and_data(self.request[key])
                file_data = type_and_data[1]
                file_type = type_and_data[0]
                return base64.b64encode(base64.b64decode(file_data)) == file_data
            except Exception:
                self.handle_validation_error('Invalid file base64 data.')


    def max_file_size(self, key, config):
        if ('max_file_size' in config and key in self.request and self.request[key] != ''):

            # TODO: get max file size from config file

            if (int(Helper.get_base64_size(self.request[key])) > int(app_config['MAX_UPLOAD_SIZE'])):
                self.handle_validation_error('The file size cannot exceed 5 MB.')


    def valid_file_types(self, key, config):
        if ('valid_file_types' in config and key in self.request and self.request[key] != ''):
            try:
                file_type_data = Helper.get_file_type_and_data(self.request[key])
                file_type = file_type_data[0]
                valid_types = Helper.get_valid_mimetypes()
                if (file_type not in valid_types):
                    self.handle_validation_error('Invalid file type.')
            except Exception as e:
                self.handle_validation_error(str(e))  

    
    def is_valid(self, *args, **kwargs):
        for key in self.validate_config:
            config = self.validate_config[key]
            
            # run validations
            self.has_key(key, config)
            if (self.complete_key_list):
                self.is_empty(key, config)
                self.is_empty_on_create(key, config, kwargs)
                self.max_length(key, config)
                self.min_length(key, config)
                self.is_integer(key, config)
                self.is_boolean(key, config)
                self.is_unique(key, config, kwargs)
                self.is_file(key, config)
                self.max_file_size(key, config)
                self.valid_file_types(key, config)

        return not self.has_error


    def get_errors(self):
        return self.errors