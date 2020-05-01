class ValidatorBase():

    def validate_required_fields(self):
        for field in self.required_fields:
            if not self.has_field(field):
                self.errors.append(
                    {
                        'message': 'The request object does not have the field: ' + field
                    }
                )
                self.has_error = True
    

    def has_field(self, field):
        if not self.request.get(field) and self.request.get(field) != '' and self.request.get(field) != []:
            return False
        else:
            return True

    
    def is_valid(self):
        self.validate_required_fields()
        return not self.has_error


    def get_errors(self):
        return self.errors