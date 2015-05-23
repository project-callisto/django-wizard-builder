from django.shortcuts import redirect, render
from reports.models import Report

def home_page(request):
    if request.method == 'POST':
        Report.objects.create(text=request.POST['report_text'])
        return redirect('/reports/the-only-report-in-the-world/')

    reports = Report.objects.all()
    return render(request, 'home.html', {'reports': reports})

def view_report(request):
    reports = Report.objects.all()
    return render(request, 'home.html', {'reports': reports})