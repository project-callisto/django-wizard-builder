from django.shortcuts import redirect, render
from reports.models import Report, Profile

def home_page(request):
    return render(request, 'home.html')

def view_profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    return render(request, 'profile.html', {'profile': profile})

def new_profile(request):
    profile = Profile.objects.create()
    Report.objects.create(text=request.POST['report_text'], profile=profile)
    return redirect('/profiles/%d/' % (profile.id,))

def add_report(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    Report.objects.create(text=request.POST['report_text'], profile=profile)
    return redirect('/profiles/%d/' % (profile.id,))
