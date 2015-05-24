from django.conf.urls import include, url
from django.contrib import admin

from reports import views

urlpatterns = [
    # Examples:
    url(r'^$', 'reports.views.home_page', name='home'),
    url(r'profiles/new$', views.new_profile, name='new_profile'),
    url(r'^profiles/(\d+)/$', views.view_profile, name='view_profile'),
    url(r'^profiles/(\d+)/add_report$', views.add_report, name='add_report'),
    #url(r'^admin/', include(admin.site.urls)),
]
