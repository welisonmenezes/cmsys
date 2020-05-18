import unittest
import json
from Utils import ErrorHandler

class TestBase(unittest.TestCase):

    def setUp(self):
        pass


    def test_ErrorHandler_get_error__string(self):
        payload_1 = 200
        payload_2 = 'Lorem ipsum dolor.'
        payload_3 = 200
        
        error = ErrorHandler().get_error(200, 'Lorem ipsum dolor.')

        response_1 = int(error[0]['error'])
        response_2 = error[0]['message']
        response_3 = int(error[1])

        self.assertEqual(payload_1, response_1, 'ErrorHandler().get_error does not return 200.')
        self.assertEqual(payload_2, response_2, 'ErrorHandler().get_error does not return \'Lorem ipsum dolor.\'.')
        self.assertEqual(payload_3, response_3, 'ErrorHandler().get_error does not return 200.')

    
    def test_ErrorHandler_get_error__list(self):
        payload_1 = 200
        payload_2 = 'message one'
        payload_3 = 200
        
        error = ErrorHandler().get_error(200, ['message one', 'message two'])

        response_1 = int(error[0]['error'])
        response_2 = error[0]['message'][0]
        response_3 = int(error[1])

        self.assertEqual(payload_1, response_1, 'ErrorHandler().get_error does not return 200.')
        self.assertEqual(payload_2, response_2, 'ErrorHandler().get_error does not return \'Lorem ipsum dolor.\'.')
        self.assertEqual(payload_3, response_3, 'ErrorHandler().get_error does not return 200.')


    def tearDown(self):
        pass