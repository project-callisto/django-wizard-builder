from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from reports.models import Report, Profile

def home_page(request):
    return render(request, 'home.html')

def view_profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    if request.method == 'POST':
        Report.objects.create(text=request.POST['report_text'], profile=profile)
        return redirect('/profiles/%d/' % (profile.id,))
    return render(request, 'profile.html', {'profile': profile})

def new_profile(request):
    profile = Profile.objects.create()
    report = Report(text=request.POST['report_text'], profile=profile)
    try:
        report.full_clean()
        report.save()
    except ValidationError:
        profile.delete()
        error = "You can't have an empty report"
        return render(request, 'home.html', {"error": error})
    return redirect('/profiles/%d/' % (profile.id,))
