import base64
from app import app_config
from Utils import Helper, Checker

class ValidatorBase():
    """Has methods to applay any configured validations from its children classes."""


    def handle_validation_error(self, message):
        """Sets has_error as true if any validaton was fail. 
            Also appends to the errors array the errors message."""

        self.errors.append({ 'message': message })
        self.has_error = True


    def has_key(self, key, config):
        """Checks if request object has the required key as settled at configuration."""

        if ('key_required' in config and config['key_required']):
            if (not key in self.request):
                self.handle_validation_error('The request object does not have the field: \'' + key + '\'.')
                self.complete_key_list = False

    
    def is_empty_on_create(self, key, config, extra_args):
        """Validates if the field is empty only during the post request."""

        if ('field_required_only_post' in config and config['field_required_only_post'] and key in self.request):
            if ('id' not in extra_args):
                if (not self.request[key] and self.request[key] == ''):
                    self.handle_validation_error('The field \'' + key + '\' cannot be empty.')

    
    def is_empty(self, key, config):
        """Validates if the field is empty for any request."""

        if ('field_required' in config and config['field_required'] and key in self.request):
            if (not self.request[key] and self.request[key] == ''):
                self.handle_validation_error('The field \'' + key + '\' cannot be empty.')


    def max_length(self, key, config):
        """Validates if the field has length greater than max length configured."""

        if ('max_length' in config and isinstance(config['max_length'], int) and key in self.request):
            if (len(str(self.request[key])) > config['max_length']):
                self.handle_validation_error('The field \'' + key + '\' length cannot be greater than ' + str(config['max_length']) + '.')


    def min_length(self, key, config):
        """Validates if the field has length less than min length configured."""

        if ('min_length' in config and isinstance(config['min_length'], int) and key in self.request):
            if (len(str(self.request[key])) < config['min_length']):
                self.handle_validation_error('The field \'' + key + '\' length cannot be less than ' + str(config['min_length']) + '.')


    def is_integer(self, key, config):
        """Validates if the field has a integer value."""

        if ('is_integer' in config and isinstance(config['is_integer'], int) and key in self.request):
            if (not isinstance(self.request[key], int)):
                self.handle_validation_error('The field \'' + key + '\' must be an integer.')

    
    def is_boolean(self, key, config):
        """Validates if the field has a boolean value."""

        if ('is_boolean' in config and isinstance(config['is_boolean'], int) and key in self.request):
            if (not isinstance(self.request[key], int) or self.request[key] < 0 or self.request[key] > 1):
                self.handle_validation_error('The field \'' + key + '\' only accpet 0 or 1 value.')


    def is_unique(self, key, config, extra_args):
        """Validates if the field already exists at the given model settled at 
            attribute model at child class."""

        if ('is_unique' in config and isinstance(config['is_unique'], int) and key in self.request):
            el = self.session.query(self.model).filter(getattr(self.model, key)==self.request[key]).first()

            if (el):
                if ('id' in extra_args):
                    if (getattr(el, key) == self.request[key]):
                        if (not extra_args['id'] or int(extra_args['id']) != int(el.id)):
                            self.handle_validation_error('The field \'' + key + '\' already exists in database.')
                else:        
                    self.handle_validation_error('The field \'' + key + '\' already exists in database.')

    
    def is_file(self, key, config):
        """Validates if the field has valid base64 data."""

        if ('is_file' in config and key in self.request and self.request[key] != ''):
            try:
                type_and_data = Helper().get_file_type_and_data(self.request[key])
                file_data = type_and_data[1]
                file_type = type_and_data[0]
                return base64.b64encode(base64.b64decode(file_data)) == file_data
            except Exception:
                self.handle_validation_error('Invalid file base64 data.')

    
    def is_datetime(self, key, config):
        
        if ('is_datetime' in config and key in self.request and self.request[key] != ''):
            if not Checker().is_datetime(self.request[key]):
                self.handle_validation_error('Datetime invalid at field: ' + key + '.')


    def max_file_size(self, key, config):
        """Validates if the field has valid base64 size."""

        if ('max_file_size' in config and key in self.request and self.request[key] != ''):
            if (int(Helper().get_base64_size(self.request[key])) > int(app_config['MAX_UPLOAD_SIZE'])):
                self.handle_validation_error('The file size cannot exceed 5 MB.')


    def valid_file_type(self, key, config):
        """Validates if the field has valid base64 mimetype."""

        if ('valid_file_type' in config and key in self.request and self.request[key] != ''):
            try:
                file_type_data = Helper().get_file_type_and_data(self.request[key])
                file_type = file_type_data[0]
                valid_types = Helper().get_valid_mimetypes()
                if (file_type not in valid_types):
                    self.handle_validation_error('Invalid file type.')
            except Exception as e:
                self.handle_validation_error(str(e))


    def valid_file_extension(self, key, config):
        """Validates if the field has valid file extension."""

        if ('valid_file_extension' in config and key in self.request and self.request[key] != ''): 
            extensions = Helper().get_valid_extensions()
            if (self.request[key] not in extensions):
                self.handle_validation_error('Invalid file extension.')


    def valid_values(self, key, config):
        """Validates if the field has a values in according with the tuple of acceptable values."""

        if ('valid_values' in config and key in self.request and self.request[key] != ''):
            if (isinstance(config['valid_values'], list)):
                if (self.request[key] not in config['valid_values']):
                    self.handle_validation_error('The field: \''+ key +'\' only accepts the following values: ' + str(config['valid_values']))

    
    def is_valid(self, *args, **kwargs):
        """Runs all validations methods applying only that was configured by the child class."""

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
                self.valid_file_type(key, config)
                self.valid_file_extension(key, config)
                self.valid_values(key, config)
                self.is_datetime(key, config)

        return not self.has_error


    def get_errors(self):
        """Gets all errors that has occurred."""

        return self.errors