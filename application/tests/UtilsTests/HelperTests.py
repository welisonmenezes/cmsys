import unittest
import json
import datetime
import base64
from app import app
from Utils import Helper

class HelperTests(unittest.TestCase):

    def setUp(self):
        self.file_b64 = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='


    def test_Helper_get_date_from_string(self):

        payload = datetime.datetime(2020, 1, 1, 0, 0, 0)
        response = Helper().get_date_from_string('2020-01-01T00:00:00')
        self.assertEqual(payload, response, 'Helper().get_date_from_string does not return a Datetime.')


    def test_Helper_get_current_datetime(self):

        payload = datetime.datetime.now()
        response = Helper().get_current_datetime()
        self.assertEqual(payload, response, 'Helper().get_current_datetime does not return the current datetime.')

    
    def test_Helper_get_base64_size(self):

        payload = 70
        response = Helper().get_base64_size(self.file_b64)
        self.assertEqual(payload, response, 'Helper().get_base64_size does not return the current datetime.')


    def test_Helper_get_file_type_and_data(self):

        payload_1 = 'image/png'
        payload_2 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
        file_info = Helper().get_file_type_and_data(self.file_b64)
        response_1 = file_info[0]
        response_2 = file_info[1]
        self.assertEqual(payload_1, response_1, 'Helper().get_file_type_and_data does not return the \'image/png\'.')
        self.assertEqual(payload_2, response_2, 'Helper().get_file_type_and_data does not return the correct binary info.')


    def test_Helper_get_extension_by_type(self):

        payload = 'png'
        response = Helper().get_extension_by_type('image/png')
        self.assertEqual(payload, response, 'Helper().get_extension_by_type does not return \'png\'.')


    def test_Helper_get_valid_mimetypes(self):

        payload = app.config['VALID_MIMETYPES'].keys()
        response = Helper().get_valid_mimetypes()
        self.assertEqual(payload, response, 'Helper().get_valid_mimetypes does not match with the VALID_MIMETYPES.')


    def test_Helper_get_valid_extensions(self):

        payload = len(app.config['VALID_MIMETYPES'].values())
        response = len(Helper().get_valid_extensions())
        self.assertEqual(payload, response, 'Helper().get_valid_extensions does not match with the VALID_MIMETYPES.')


    def test_Helper_get_file_details_from_request(self):
        data = {
            'file': self.file_b64
        }
        payload = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==')
        response = Helper().get_file_details_from_request(data)['data']
        self.assertEqual(payload, response, 'Helper().get_file_details_from_request does not match the binary data.')


    def test_Helper_get_null_if_empty(self):

        payload = None
        response = Helper().get_null_if_empty('')
        self.assertEqual(payload, response, 'Helper().get_null_if_empty does not return None.')


    def test_Helper_get_with_slug(self):
        data = {
            'name': 'JOão Caçou a RÃ à noite'
        }
        payload = 'joao-cacou-a-ra-a-noite'
        response = Helper().get_with_slug(data, 'name')['name']
        self.assertEqual(payload, response, 'Helper().get_with_slug does not return \'joao-cacou-a-ra-a-noite\'.')
    

    def tearDown(self):
        pass