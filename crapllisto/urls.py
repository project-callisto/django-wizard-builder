from django.conf.urls import include, url
from django.contrib import admin

from reports import views

urlpatterns = [
    # Examples:
    url(r'^$', 'reports.views.home_page', name='home'),
    url(r'^reports/the-only-report-in-the-world/$', views.view_report, name='view_report'),

    #url(r'^admin/', include(admin.site.urls)),
]
