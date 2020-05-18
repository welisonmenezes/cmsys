import unittest
from sqlalchemy import MetaData
from app import app
from Models import Base, Engine
from Utils import Checker

def truncate_db():
    meta = MetaData(bind=Engine)
    con = Engine.connect()
    trans = con.begin()
    con.execute('SET FOREIGN_KEY_CHECKS = 0;')
    for table in meta.sorted_tables:
        con.execute(table.delete())
    con.execute('SET FOREIGN_KEY_CHECKS = 1;')
    trans.commit()


class TestBase(unittest.TestCase):

    def setUp(self):
        pass


    def test_Checker_can_be_integer__true(self):
        payload = True
        response = Checker().can_be_integer(10)
        self.assertEqual(payload, response, 'Checker().can_be_integer does not return True.')

    
    def test_Checker_can_be_integer__false(self):
        payload = False
        response = Checker().can_be_integer('Not Integer')
        self.assertEqual(payload, response, 'Checker().can_be_integer does not return False.')


    def test_Checker_is_image_type__true(self):
        payload = True
        response = Checker().is_image_type('image/png')
        self.assertEqual(payload, response, 'Checker().is_image_type does not return True.')

    
    def test_Checker_is_image_type__false(self):
        payload = False
        response = Checker().is_image_type('Not Mimetype')
        self.assertEqual(payload, response, 'Checker().is_image_type does not return False.')

    
    def test_Checker_is_datetime__true(self):
        payload = True
        response = Checker().is_datetime('2020-01-01 00:00:00')
        self.assertEqual(payload, response, 'Checker().is_datetime does not return True.')

    
    def test_Checker_is_datetime__false(self):
        payload = False
        response = Checker().is_datetime('2020/01/01 00:00:00')
        self.assertEqual(payload, response, 'Checker().is_datetime does not return False.')

    
    def test_Checker_is_first_date_smaller__true(self):
        payload = True
        response = Checker().is_first_date_smaller('2019-01-01 00:00:00', '2020-01-01 00:00:00')
        self.assertEqual(payload, response, 'Checker().is_first_date_smaller does not return True.')

    
    def test_Checker_is_first_date_smaller__false(self):
        payload = False
        response = Checker().is_first_date_smaller('2020-01-01 00:00:00', '2019-01-01 00:00:00')
        self.assertEqual(payload, response, 'Checker().is_first_date_smaller does not return False.')


    def tearDown(self):
        pass
        #truncate_db()