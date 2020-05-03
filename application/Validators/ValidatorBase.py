class ValidatorBase():

    def handle_validation_error(self, message):
        self.errors.append({ 'message': message })
        self.has_error = True


    def has_key(self, key, config):
        if ('key_required' in config and config['key_required']):
            if (not self.request.get(key) and self.request.get(key) != '' and self.request.get(key) != []):
                self.handle_validation_error('The request object does not have the field: \'' + key + '\'.')

    
    def is_empty(self, key, config):
        if ('field_required' in config and config['field_required']):
            if (not self.request[key] and self.request[key] == ''):
                self.handle_validation_error('The field \'' + key + '\' cannot be empty.')

    
    def is_valid(self):

        for key in self.validate_config:
            config = self.validate_config[key]
            
            # run validations
            self.has_key(key, config)
            self.is_empty(key, config)

        return not self.has_error


    def get_errors(self):
        return self.errors