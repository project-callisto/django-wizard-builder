from django.shortcuts import redirect, render
from reports.models import Report

def home_page(request):
    if request.method == 'POST':
        Report.objects.create(text=request.POST['report_text'])
        return redirect('/')

    reports = Report.objects.all()
    return render(request, 'home.html', {'reports': reports})