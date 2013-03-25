from django.test import LiveServerTestCase
from django.conf import settings
from splinter import Browser


class GridTestcase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = Browser()  #'remote', **settings.SELENIUM_GRID)
        super(GridTestcase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(GridTestcase, cls).tearDownClass()


from e2e_login_logout import FeatureLogin
from e2e_registration import FeatureRegistration
