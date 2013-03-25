from waffle.models import Switch
from app.tests import GridTestcase


class FeatureRegistration(GridTestcase):
    """ Feature: Registering a user """

    def setUp(self):
        # Create the login switch
        self.switch, created = Switch.objects.get_or_create(name="Registration", active=True, note='')

    def visit(self, rel_url):
        self.browser.visit('%s%s' % (self.live_server_url, rel_url))

    def test_registration_link(self):
        """ Given I am on the homepage """
        self.visit('/')

        """ When I click the register button """
        self.browser.find_by_id('registerbtn').click()

        """ Then I should see the registration page """
        self.assertEquals(self.browser.is_text_present('Create My Account'), True)

    def test_register_user(self):
        """ Given I am on the registration page """
        self.visit('/#/register')

        """ When I fill in the user details and submit """
        self.browser.fill('username', 'test_user1')
        self.browser.fill('email', 'test@example.com')
        self.browser.fill('passwd', 'password')
        self.browser.fill('conpasswd', 'password')
        self.browser.find_by_id('register_submit').click()

        """ Then I will be logged in """
        self.assertEquals(self.browser.is_text_present('test_user1'), True)

    def test_register_conflict(self):
        """ Given a user """
        self.test_register_user()

        """ When I try to register a user with the same username or email """
        self.test_register_user()

        """ Then there will be an error message """
        self.assertEquals(self.browser.is_text_present('Username/email is already in use'), True)
