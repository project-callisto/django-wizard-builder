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

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['report_text'] = 'A new report'

        response = home_page(request)

        self.assertIn('A new report', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'report_text':  'A new report'}
        )
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