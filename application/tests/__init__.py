
import unittest
from app import app
from .UtilsTests import CheckerTests, ErrorHandlerTests, FilterBuilderTests, HelperTests, PaginateTestes

def load_tests(loader, tests, pattern):
    if app.config['SQLALCHEMY_DATABASE_URI'] != 'mysql+pymysql://root:@localhost/cmsys_tests':
        raise Exception('The database must be from the test environment.')

    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromModule(CheckerTests))
    suite.addTests(loader.loadTestsFromModule(ErrorHandlerTests))
    suite.addTests(loader.loadTestsFromModule(FilterBuilderTests))
    suite.addTests(loader.loadTestsFromModule(HelperTests))
    suite.addTests(loader.loadTestsFromModule(PaginateTestes))
    return suite