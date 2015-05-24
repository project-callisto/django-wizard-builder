from django.conf.urls import include, url

from reports import views as report_views
from reports import urls as report_urls

urlpatterns = [
    # Examples:
    url(r'^$', 'reports.views.home_page', name='home'),
    url(r'profiles/', include(report_urls)),
    #url(r'^admin/', include(admin.site.urls)),
]
