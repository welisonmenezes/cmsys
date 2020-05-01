class ValidatorBase():

    def validate_required_keys(self):
        for field in self.required_keys:
            if not self.has_key(field):
                self.errors.append(
                    {
                        'message': 'The request object does not have the field: \'' + field + '\'.'
                    }
                )
                self.has_error = True
    

    def has_key(self, field):
        if not self.request.get(field) and self.request.get(field) != '' and self.request.get(field) != []:
            return False
        else:
            return True


    def validate_required_fields(self):
        for field in self.required_fields:
            if (not self.has_key(field)):
                continue
            if self.is_empty(field):
                self.errors.append(
                    {
                        'message': 'The field \'' + field + '\' cannot be empty.'
                    }
                )
                self.has_error = True

    
    def is_empty(self, field):
        if not self.request[field] and self.request[field] == '':
            return True
        return False

    
    def is_valid(self):
        self.validate_required_keys()
        self.validate_required_fields()
        return not self.has_error


    def get_errors(self):
        return self.errors