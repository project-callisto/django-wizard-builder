from django.test import TestCase

from reports.forms import EMPTY_REPORT_ERROR, ReportForm
from reports.models import Profile, Report

class ReportFormTest(TestCase):

    def test_form_report_input_has_placeholder_and_css_classes(self):
        form = ReportForm()
        self.assertIn('placeholder="Write it down"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_reports(self):
        form = ReportForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_REPORT_ERROR]
        )

    def test_form_save_handles_saving_to_a_profile(self):
        profile = Profile.objects.create()
        form = ReportForm(data={'text': 'something happened'})
        new_report = form.save(for_profile=profile)
        self.assertEqual(new_report, Report.objects.first())
        self.assertEqual(new_report.text, 'something happened')
        self.assertEqual(new_report.profile, profile)
