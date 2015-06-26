from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
User = get_user_model()
from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest


class DashboardTest(FunctionalTest):

    def create_pre_authenticated_session(self, username, password):
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