from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from reports.views import home_page
from reports.models import Report

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

class ReportModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_report = Report()
        first_report.text = 'The first report ever'
        first_report.save()

        second_report = Report()
        second_report.text = 'Report number two'
        second_report.save()

        saved_reports = Report.objects.all()
        self.assertEqual(saved_reports.count(), 2)

        first_saved_report = saved_reports[0]
        second_saved_report = saved_reports[1]
        self.assertEqual(first_saved_report.text, 'The first report ever')
        self.assertEqual(second_saved_report.text, 'Report number two')

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/reports/the-only-report-in-the-world/')
        self.assertTemplateUsed(response, 'report.html')

    def test_displays_all_items(self):
        Report.objects.create(text='reporty 1')
        Report.objects.create(text='reporty 2')

        response = self.client.get('/reports/the-only-report-in-the-world/')

        self.assertContains(response, 'reporty 1')
        self.assertContains(response, 'reporty 2')

class NewListTest(TestCase):
    def test_home_page_can_save_a_POST_request(self):
        self.client.post(
            '/reports/new',
            data={'report_text': 'A new report'}
        )
        self.assertEqual(Report.objects.count(), 1)
        new_report = Report.objects.first()
        self.assertEqual(new_report.text, 'A new report')

    def test_home_page_redirects_after_POST(self):
        response = self.client.post(
            '/reports/new',
            data={'report_text': 'A new report'}
        )
        self.assertRedirects(response, '/reports/the-only-report-in-the-world/')
