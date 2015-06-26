from django.core.exceptions import ValidationError
from django.test import TestCase
from reports.models import Report, Profile

class ProfileModelTest(TestCase):

    def test_default_text(self):
        report = Report()
        self.assertEqual(report.text, '')

class ReportModelTest(TestCase):

    def test_report_is_related_to_profile(self):
        profile = Profile.objects.create()
        report = Report()
        report.profile = profile
        report.save()
        self.assertIn(report, profile.report_set.all())

    def test_cannot_save_empty_reports(self):
        profile = Profile.objects.create()
        report = Report(profile = profile, text='')
        with self.assertRaises(ValidationError):
            report.save()
            report.full_clean()

    def test_get_absolute_url(self):
        profile = Profile.objects.create()
        self.assertEqual(profile.get_absolute_url(), '/reports/%d/' % (profile.id,))

    def test_report_ordering(self):
        profile = Profile.objects.create()
        report1 = Report.objects.create(profile=profile, text='first report')
        report2 = Report.objects.create(profile=profile, text='2 report')
        report3 = Report.objects.create(profile=profile, text='report #3')
        self.assertEqual(
            list(Report.objects.all()),
            [report1, report2, report3]
        )

    def test_string_representation(self):
        report = Report(text='some report')
        self.assertEqual(str(report), 'some report')