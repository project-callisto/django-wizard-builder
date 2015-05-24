from django.shortcuts import redirect, render
from reports.models import Report, Profile

def home_page(request):
    return render(request, 'home.html')

def view_profile(request):
    reports = Report.objects.all()
    return render(request, 'profile.html', {'reports': reports})

def new_profile(request):
    profile = Profile.objects.create()
    Report.objects.create(text=request.POST['report_text'], profile=profile)
    return redirect('/profiles/the-only-profile-in-the-world/')