from .base import FunctionalTest
from selenium.webdriver.support.ui import WebDriverWait

class LoginTest(FunctionalTest):

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id)
        )

    def test_signup(self):
        # Edith goes to the awesome Callisto site
        # and notices a "Sign in" link for the first time.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_signup').click()

        # A login screen appears
        edith_signup_url = self.browser.current_url
        self.assertRegex(edith_signup_url, '/signup/')

        # Edith signs up with her email address
        self.browser.find_element_by_id(
            'id_username'
        ).send_keys('edith@notrealemail.com')
        self.browser.find_element_by_id(
            'id_password1'
        ).send_keys('password')
        self.browser.find_element_by_id(
            'id_password2'
        ).send_keys('password')
        self.browser.find_element_by_tag_name('button').click()

        # She can see that she is logged in
        self.wait_for_element_with_id('id_logout')
        # She is on an interstitial page explaining record
        encouragement = self.browser.find_element_by_id('.encouragement')
        self.assertIn("Now we'll begin", encouragement.text)