from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

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

class ProfileAndReportModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        profile = Profile()
        profile.save()

        first_report = Report()
        first_report.text = 'The first report ever'
        first_report.profile = profile
        first_report.save()

        second_report = Report()
        second_report.text = 'Report number two'
        second_report.profile = profile
        second_report.save()

        saved_profile = Profile.objects.first()
        self.assertEqual(saved_profile, profile)

        saved_reports = Report.objects.all()
        self.assertEqual(saved_reports.count(), 2)

        first_saved_report = saved_reports[0]
        second_saved_report = saved_reports[1]
        self.assertEqual(first_saved_report.text, 'The first report ever')
        self.assertEqual(first_saved_report.profile, profile)
        self.assertEqual(second_saved_report.text, 'Report number two')
        self.assertEqual(second_saved_report.profile, profile)

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

class NewReportTest(TestCase):
    def test_can_save_a_POST_request_to_existing_profile(self):
        other_profile = Profile.objects.create()
        correct_profile = Profile.objects.create()

        self.client.post(
            '/profiles/%d/add_report' % correct_profile.id,
            data={'report_text':'A new report for an existing profile'}
        )

        self.assertEqual(Report.objects.count(), 1)
        new_report = Report.objects.first()
        self.assertEqual(new_report.text, 'A new report for an existing profile')
        self.assertEqual(new_report.profile, correct_profile)

    def test_redirects_to_profile_view(self):
        other_profile = Profile.objects.create()
        correct_profile = Profile.objects.create()

        response = self.client.post(
            '/profiles/%d/add_report' % correct_profile.id,
            data={'report_text':'A new report for an existing profile'}
        )

        self.assertRedirects(response, 'profiles/%d/' % correct_profile.id)