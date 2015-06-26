from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
User = get_user_model()
from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest


class DashboardTest(FunctionalTest):

    def create_pre_authenticated_session(self, username, password):
        if self.against_staging:
            #sign up & log in manually YOLO
            self.browser.get(self.server_url + '/signup')
            self.browser.find_element_by_id('id_username').send_keys(username)
            self.browser.find_element_by_id('id_password1').send_keys(password)
            self.browser.find_element_by_id('id_password2').send_keys(password)
            self.browser.find_element_by_tag_name('button').click()

            self.browser.get(self.server_url + '/login')
            self.browser.find_element_by_id('id_username').send_keys(username)
            self.browser.find_element_by_id('id_password').send_keys(password)
            self.browser.find_element_by_tag_name('button').click()
            self.wait_for_element_with_id('id_logout')

        else:
            user = User.objects.create_user(username=username,
                                       password=password)
            self.client.login(username=username, password=password)
            cookie = self.client.cookies['sessionid']
            ## to set a cookie we need to first visit the domain.
            ## 404 pages load the quickest!
            self.browser.get(self.server_url + "/404_no_such_url/")
            self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})

    def test_logged_in_users_reports_are_saved_on_dashboard(self):
        self.browser.get(self.server_url)
        self.wait_to_be_logged_out()

        # Edith is a logged-in user
        self.create_pre_authenticated_session('edith', 'somePa55word')

        self.browser.get(self.server_url)
        self.wait_to_be_logged_in()