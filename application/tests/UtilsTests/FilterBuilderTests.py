import unittest
import json
from Utils import FilterBuilder
from Models import Post, Language

class TestBase(unittest.TestCase):

    def setUp(self):
        self.args = {
            'name': 'a',
            'title': 'b',
            'status': 'c',
            'created': '2020-01-01T00:00:00',
            'page': 1,
            'limit': 10,
            'order_by': 'id',
            'order': 'desc'
        }
        self.kwa = {}
        self.fb = FilterBuilder(Post, self.args)


    def test_FilterBuilder_get_context_attr__default(self):
        payload = Post.id
        response = self.fb.get_context_attr('id', self.kwa)
        self.assertEqual(payload, response, 'ErrorHandler().get_context_attr does not return \'Post.id\'.')

    
    def test_FilterBuilder_get_context_attr__joined(self):
        kwa = {
            'joined': Language,
            'joined_key': 'id'
        }
        fb = FilterBuilder(Post, self.args)

        payload = Language.id
        response = fb.get_context_attr('id', kwa)
        self.assertEqual(payload, response, 'ErrorHandler().get_context_attr does not return \'Language.id\'.')


    def test_FilterBuilder_set_equals_filter(self):

        payload = '"Post".name = :name_1'
        self.fb.set_equals_filter('name')
        response = str(self.fb.filter[0])
        self.assertEqual(payload, response, 'ErrorHandler().set_equals_filter does not return \'"Post".name = :name_1\'.')


    def test_FilterBuilder_set_like_filter(self):

        payload = '"Post".name LIKE :name_1'
        self.fb.set_like_filter('name')
        response = str(self.fb.filter[0])
        self.assertEqual(payload, response, 'ErrorHandler().set_like_filter does not return \'"Post".name LIKE :name_1\'.')


    def test_FilterBuilder_set_and_or_filter(self):

        payload = '"Post".name LIKE :name_1 OR "Post".status LIKE :status_1'
        self.fb.set_and_or_filter('name', 'or', [{'field':'name', 'type':'like'}, {'field':'status', 'type':'like'}])
        response = str(self.fb.filter[0])
        self.assertEqual(payload, response, 'ErrorHandler().set_and_or_filter does not return \'"Post".name LIKE :name_1 OR "Post".type LIKE :type_1\'.')


    def test_FilterBuilder_set_and_or_filter_exception(self):

        payload = Exception
        response = None

        try:
            self.fb.set_and_or_filter('name', 'or', [{'field':'xxx', 'type':'like'}, {'field':'xxx', 'type':'like'}])
        except Exception as e:
            response = type(e)

        self.assertEqual(payload, response, 'ErrorHandler().set_and_or_filter does not return an Exception.')


    def test_FilterBuilder_set_date_filter(self):

        payload = '"Post".created >= :created_1'
        self.fb.set_date_filter('created')
        response = str(self.fb.filter[0])
        self.assertEqual(payload, response, 'ErrorHandler().set_date_filter does not return \'"Post".created >= :created_1\'.')


    def test_FilterBuilder_set_date_filter__exception(self):

        payload = Exception
        response = None

        try:
            self.fb.set_date_filter('name')
        except Exception as e:
            response = type(e)

        self.assertEqual(payload, response, 'ErrorHandler().set_date_filter does not return an Exception.')

    
    def test_FilterBuilder_set_between_dates_filter(self):

        payload = '"Post".created BETWEEN :created_1 AND :created_2'
        self.fb.set_between_dates_filter('created', compare_date_time_one='2020-01-01T00:00:00', compare_date_time_two='2020-01-01T00:00:00')
        response = str(self.fb.filter[0])
        self.assertEqual(payload, response, 'ErrorHandler().set_between_dates_filter does not return \'"Post".created BETWEEN :created_1 AND :created_2\'.')

    
    def test_FilterBuilder_set_between_dates_filter__not_between(self):
        
        payload = '"Post".created NOT BETWEEN :created_1 AND :created_2'
        self.fb.set_between_dates_filter('created', compare_date_time_one='2020-01-01T00:00:00', compare_date_time_two='2020-01-01T00:00:00', not_between='1')
        response = str(self.fb.filter[0])
        self.assertEqual(payload, response, 'ErrorHandler().set_between_dates_filter does not return \'"Post".created BETWEEN :created_1 AND :created_2\'.')


    def test_FilterBuilder_set_between_dates_filter__exception(self):
        
        payload = Exception
        response = None

        try:
            self.fb.set_between_dates_filter('created', compare_date_time_one='2020-01-01T00:00:00', compare_date_time_two='xxxx')
        except Exception as e:
            response = type(e)

        self.assertEqual(payload, response, 'ErrorHandler().set_between_dates_filter does not return an Exception.')


    def test_FilterBuilder_get_filter(self):
        
        payload = ()
        response = self.fb.get_filter()
        self.assertEqual(payload, response, 'ErrorHandler().get_filter does not return a tuple.')

    
    def test_FilterBuilder_get_page(self):
        
        payload = 1
        response = self.fb.get_page()
        self.assertEqual(payload, response, 'ErrorHandler().get_page does not return  1.')

    
    def test_FilterBuilder_get_limit(self):
        
        payload = 10
        response = self.fb.get_limit()
        self.assertEqual(payload, response, 'ErrorHandler().get_limit does not return  10.')

    
    def test_FilterBuilder_get_order_by(self):
        
        payload = '"Post".id DESC'
        response = str(self.fb.get_order_by()[0])
        self.assertEqual(payload, response, 'ErrorHandler().get_order_by does not return  \'"Post".id DESC\'.')


    def tearDown(self):
        pass