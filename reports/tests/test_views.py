from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, SESSION_KEY
from unittest.mock import patch
User = get_user_model()

from reports.views import home_page
from reports.models import Report, Profile
from reports.forms import ReportForm, EMPTY_REPORT_ERROR

class HomePageTest(TestCase):

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ReportForm)

class SignupViewTest(TestCase):
    def test_signup_page_renders_signup_template(self):
        response = self.client.get('/signup')
        self.assertTemplateUsed(response, 'signup.html')

    def test_displays_signup_form(self):
        response = self.client.get('/signup')
        self.assertIsInstance(response.context['form'], UserCreationForm)
        self.assertContains(response, 'name="username"')

    @patch('django.contrib.auth.authenticate')
    def test_signup_calls_authenticate(
        self, mock_authenticate
    ):
        mock_authenticate.return_value = None
        self.client.post('/signup',
                         {'username': 'test1',
                          'password1': 'password',
                          'password2': 'password'})
        mock_authenticate.assert_called_once()

    @patch('django.contrib.auth.authenticate')
    def test_user_gets_logged_in_after_signup(
            self, mock_authenticate
    ):
        mock_authenticate.side_effect = lambda: User.objects.get(username='test')
        response = self.client.post('/signup',
                         {'username': 'test',
                          'password1': 'password',
                          'password2': 'password'})
        self.assertEqual(response.client.session[SESSION_KEY], str(User.objects.get(username="test").pk))

class LoginViewTest(TestCase):
    def test_login_page_renders_login_template(self):
        response = self.client.get('/login')
        self.assertTemplateUsed(response, 'login.html')

    def test_displays_login_form(self):
        response = self.client.get('/login')
        self.assertIsInstance(response.context['form'], AuthenticationForm)
        self.assertContains(response, 'name="username"')

class ProfileViewTest(TestCase):
    def test_uses_profile_template(self):
        profile = Profile.objects.create()
        response = self.client.get('/profiles/%d/' % (profile.id,))
        self.assertTemplateUsed(response, 'profile.html')

    def test_displays_only_reports_for_that_profile(self):
        correct_profile = Profile.objects.create()
        Report.objects.create(text='reporty 1', profile=correct_profile)
        Report.objects.create(text='reporty 2', profile=correct_profile)
        other_profile = Profile.objects.create()
        Report.objects.create(text='other reporty 1', profile=other_profile)
        Report.objects.create(text='other reporty 2', profile=other_profile)

        response = self.client.get('/profiles/%d/' % (correct_profile.id,))

        self.assertContains(response, 'reporty 1')
        self.assertContains(response, 'reporty 2')
        self.assertNotContains(response, 'other reporty 1')
        self.assertNotContains(response, 'other reporty 2')

    def test_passes_correct_profile_to_template(self):
        other_profile = Profile.objects.create()
        correct_profile = Profile.objects.create()
        response = self.client.get('/profiles/%d/' % (correct_profile.id, ))
        self.assertEquals(response.context['profile'], correct_profile)

    def test_can_save_a_POST_request_to_existing_profile(self):
        other_profile = Profile.objects.create()
        correct_profile = Profile.objects.create()

        self.client.post(
            '/profiles/%d/' % correct_profile.id,
            data={'text':'A new report for an existing profile'}
        )

        self.assertEqual(Report.objects.count(), 1)
        new_report = Report.objects.first()
        self.assertEqual(new_report.text, 'A new report for an existing profile')
        self.assertEqual(new_report.profile, correct_profile)

    def test_POST_redirects_to_profile_view(self):
        other_profile = Profile.objects.create()
        correct_profile = Profile.objects.create()

        response = self.client.post(
            '/profiles/%d/' % correct_profile.id,
            data={'text':'A new report for an existing profile'}
        )

        self.assertRedirects(response, 'profiles/%d/' % correct_profile.id)

    def post_invalid_input(self):
        profile = Profile.objects.create()
        return self.client.post('/profiles/%d/' % (profile.id,),
                                    data={'text': ''}
                                    )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Report.objects.count(), 0)

    def test_for_invalid_input_renders_profile_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ReportForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_REPORT_ERROR))

    def test_displays_report_form(self):
        profile = Profile.objects.create()
        response = self.client.get('/profiles/%d/' % (profile.id))
        self.assertIsInstance(response.context['form'], ReportForm)
        self.assertContains(response, 'name="text"')

class NewProfileTest(TestCase):
    def test_home_page_can_save_a_POST_request(self):
        self.client.post(
            '/profiles/new',
            data={'text': 'A new report'}
        )
        self.assertEqual(Report.objects.count(), 1)
        new_report = Report.objects.first()
        self.assertEqual(new_report.text, 'A new report')

    def test_home_page_redirects_after_POST(self):
        response = self.client.post(
            '/profiles/new',
            data={'text': 'A new report'}
        )
        new_profile = Profile.objects.first()
        self.assertRedirects(response, '/profiles/%d/' % (new_profile.id,))

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/profiles/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shwon_on_home_page(self):
        response = self.client.post('/profiles/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_REPORT_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/profiles/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ReportForm)

    def test_invalid_reports_arent_saved(self):
        self.client.post('/profiles/new', data={'text':''})
        self.assertEqual(Profile.objects.count(), 0)
        self.assertEqual(Report.objects.count(), 0)
