class ValidatorBase():

    def handle_validation_error(self, message):
        self.errors.append({ 'message': message })
        self.has_error = True


    def has_key(self, key, config):
        if ('key_required' in config and config['key_required']):
            if (not self.request.get(key) and self.request.get(key) != '' and self.request.get(key) != []):
                self.handle_validation_error('The request object does not have the field: \'' + key + '\'.')
                self.complete_key_list = False

    
    def is_empty(self, key, config):
        if ('field_required' in config and config['field_required']):
            if (not self.request[key] and self.request[key] == ''):
                self.handle_validation_error('The field \'' + key + '\' cannot be empty.')


    def max_length(self, key, config):
        if ('max_length' in config and isinstance(config['max_length'], int)):
            if (len(self.request[key]) > config['max_length']):
                self.handle_validation_error('The field \'' + key + '\' length cannot be greater than ' + str(config['max_length']))


    def min_length(self, key, config):
        if ('min_length' in config and isinstance(config['min_length'], int)):
            if (len(self.request[key]) < config['min_length']):
                self.handle_validation_error('The field \'' + key + '\' length cannot be less than ' + str(config['min_length']))

    
    def is_valid(self):

        for key in self.validate_config:
            config = self.validate_config[key]
            
            # run validations
            self.has_key(key, config)
            if (self.complete_key_list):
                self.is_empty(key, config)
                self.max_length(key, config)
                self.min_length(key, config)

        return not self.has_error


    def get_errors(self):
        return self.errors