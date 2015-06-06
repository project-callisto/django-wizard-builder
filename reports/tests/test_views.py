from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from reports.views import home_page
from reports.models import Report, Profile

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

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
            data={'report_text':'A new report for an existing profile'}
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
            data={'report_text':'A new report for an existing profile'}
        )

        self.assertRedirects(response, 'profiles/%d/' % correct_profile.id)

    def test_validation_errors_end_up_on_profile_page(self):
        profile = Profile.objects.create()
        response = self.client.post('/profiles/%d/' % (profile.id,),
                                    data={'report_text': ''}    )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        expected_error = escape("You can't have an empty report")
        self.assertContains(response, expected_error)


class NewProfileTest(TestCase):
    def test_home_page_can_save_a_POST_request(self):
        self.client.post(
            '/profiles/new',
            data={'report_text': 'A new report'}
        )
        self.assertEqual(Report.objects.count(), 1)
        new_report = Report.objects.first()
        self.assertEqual(new_report.text, 'A new report')

    def test_home_page_redirects_after_POST(self):
        response = self.client.post(
            '/profiles/new',
            data={'report_text': 'A new report'}
        )
        new_profile = Profile.objects.first()
        self.assertRedirects(response, '/profiles/%d/' % (new_profile.id,))

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/profiles/new', data={'report_text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty report")
        self.assertContains(response, expected_error)

    def test_invalid_reports_arent_saved(self):
        self.client.post('/profiles/new', data={'report_text':''})
        self.assertEqual(Profile.objects.count(), 0)
        self.assertEqual(Report.objects.count(), 0)
