from django import forms

from reports.models import Report

EMPTY_REPORT_ERROR = "You can't have an empty report"

class ReportForm(forms.models.ModelForm):
    class Meta:
        model = Report
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Write it down',
                'class': 'form-control input-lg'
            })
        }
        error_messages = {
            'text': {'required': EMPTY_REPORT_ERROR}
        }