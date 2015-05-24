from django.conf.urls import include, url
from django.contrib import admin

from reports import views

urlpatterns = [
    # Examples:
    url(r'^$', 'reports.views.home_page', name='home'),
    url(r'profiles/new$', views.new_profile, name='new_report'),
    url(r'^profiles/the-only-profile-in-the-world/$', views.view_profile, name='view_report'),

    #url(r'^admin/', include(admin.site.urls)),
]
