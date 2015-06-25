from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView

from reports.models import Report, Profile
from reports.forms import ReportForm

SIGNUP_ERROR='There was an error creating your account. Please email contact@projectcallisto.org if it persists.'

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
      if user is not None and user.is_active:
        login(self.request, user)
      else:
        form.add_error(None, ValidationError(SIGNUP_ERROR, code='signup_error'))
        return self.render_to_response(self.get_context_data(form=form))
      return super(SignupView, self).form_valid(form)
