import unittest
import json
from Utils import Paginate
from Models import Session, Post

class PaginateTests(unittest.TestCase):

    def setUp(self):
        session = Session()
        query = session.query(Post.id)
        self.result = Paginate(query, 1, 10)
        self.keys = ['prev', 'next', 'has_prev', 'has_next', 'size', 'pages', 'total', 'current']


    def test_PaginateTests_init(self):
        payload = True
        response = True

        for r in self.result.pagination.keys():
            if r not in self.keys:
                response = False

        if not isinstance(self.result.items, list):
            response = False

        if self.result.pagination['current'] != 1 or self.result.pagination['size'] != 10:
            response = False

        self.assertEqual(payload, response, 'PaginateTests().__init__ does not work correctly.')


    def tearDown(self):
        pass