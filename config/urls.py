from django.conf.urls import include, url
from django.views.generic.edit import CreateView
from django.contrib.auth.views import logout, login

from reports.views import SignupView

from reports import urls as report_urls

urlpatterns = [
    # Examples:
    url(r'^$', 'reports.views.home_page', name='home'),
    url(r'^profiles/', include(report_urls)),
    url(r'^signup$', SignupView.as_view(), name='signup'),
    url(r'^logout$', logout, {'next_page': '/'}, name='logout'),
    url(r'^login$', login, {'template_name': 'login.html'}, name='login')
    #url(r'^admin/', include(admin.site.urls)),
]
