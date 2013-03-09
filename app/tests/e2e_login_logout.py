from django.test import LiveServerTestCase
from splinter import Browser
from django.contrib.auth.models import User
from waffle.models import Switch


class FeatureLogin(LiveServerTestCase):
    """ Feature: Logging in and out """

    @classmethod
    def setUpClass(cls):       
        cls.browser = Browser()
        super(FeatureLogin, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(FeatureLogin, cls).tearDownClass()

    def setUp(self):
        # Create the login switch
        self.switch, created = Switch.objects.get_or_create(name="Login", active=True, note='')

    def visit(self, rel_url):
        self.browser.visit('%s%s' % (self.live_server_url, rel_url))

    def test_login_link(self):
        """ Given I am on the homepage """
        self.visit('/')

        """ When I click the login button """
        self.browser.find_by_id('loginbtn').click()

        """ Then I should see the login page """
        self.assertEquals(self.browser.is_text_present('Please sign in'), True)

    def test_invalid_login(self):
        """ Given I am on the login page """
        self.visit('/#/login')

        """ When I fill in the user details with garbage and click submit """
        self.browser.fill('username', 'garbage username')
        self.browser.fill('password', 'garbage password')
        self.browser.find_by_id('signin').click()

        """ Then I should see a message telling me the information is invalid """
        self.assertEquals(self.browser.is_text_present('Wrong username/password'), True)

    def test_login(self):
        """ Given I have a user """
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')

        user = ('admin', 'admin')

        """ And I am on the login page """
        self.visit('/#/login')

        """ When I fill in the user details and click submit """
        self.browser.fill('username', user[0])
        self.browser.fill('password', user[1])
        self.browser.find_by_id('signin').click()

        """ Then I will be logged in """
        self.assertEquals(self.browser.is_text_present(user[0]), True)

    def test_logout(self):
        """ Given I am logged in """
        self.test_login()

        """ And I am on the homepage """
        self.visit('/')

        """ When I click logout """
        self.browser.find_by_id('logoutbtn').click()

        """ Then I will be logged out """
        self.assertEquals(self.browser.is_text_present("Login"), True)

    #def test_switch(self):
    #    """ Given the 'Login' switch is disabled """
    #    self.switch.active = False
    #    self.switch.save()

    #    """ When I try to visit the login page """
    #    self.visit('/#/login')

    #    """ Then I will not be able to access it """
    #    self.assertEquals(self.browser.is_text_present("Login"), False)

    #    """ And there will be no login link """
    #    self.assertEquals(self.browser.find_by_id('loginbtn'), None)
