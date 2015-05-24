from django.shortcuts import redirect, render
from reports.models import Report, Profile

def home_page(request):
    return render(request, 'home.html')

def view_report(request):
    reports = Report.objects.all()
    return render(request, 'report.html', {'reports': reports})

def new_report(request):
    profile = Profile.objects.create()
    Report.objects.create(text=request.POST['report_text'], profile=profile)
    return redirect('/reports/the-only-report-in-the-world/')