
import unittest
from app import app
from . import TestChecker

def load_tests(loader, tests, pattern):
    if app.config['SQLALCHEMY_DATABASE_URI'] != 'mysql+pymysql://root:@localhost/cmsys_tests':
        raise Exception('The database must be the test envoirement.')

    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromModule(TestChecker))
    return suite