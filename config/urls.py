from django.conf.urls import include, url
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from reports.views import SignupView

from reports import urls as report_urls

urlpatterns = [
    # Examples:
    url(r'^$', 'reports.views.home_page', name='home'),
    url(r'^profiles/', include(report_urls)),
    url('^signup/', SignupView.as_view(), name='signup'),
    #url(r'^admin/', include(admin.site.urls)),
]
