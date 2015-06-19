from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView

from reports.models import Report, Profile
from reports.forms import ReportForm

def home_page(request):
    return render(request, 'home.html', {'form': ReportForm()})

def view_profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    form = ReportForm()
    if request.method == 'POST':
        form = ReportForm(data=request.POST)
        if form.is_valid():
            form.save(for_profile=profile)
            return redirect(profile)
    return render(request, 'profile.html', {
        'profile': profile, 'form': form})

def new_profile(request):
    form = ReportForm(data=request.POST)
    if form.is_valid():
        profile = Profile.objects.create()
        form.save(for_profile=profile)
        return redirect(profile)
    else:
        return render(request, 'home.html', {"form": form})

class SignupView(FormView):
   template_name = 'signup.html'
   form_class = UserCreationForm
   success_url='/'

   def form_valid(self, form):
      #save the new user first
      form.save()
      #login new user
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(username=username, password=password)
      login(self.request, user)
      return super(SignupView, self).form_valid(form)
