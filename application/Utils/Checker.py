class Checker():

    @staticmethod
    def can_be_integer(element):
        try:
            int(element)
            return True
        except ValueError:
            return False