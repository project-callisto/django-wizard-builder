from django.conf.urls import url

from reports import views

urlpatterns = [
    # Examples:
    url(r'^new$', views.new_profile, name='new_profile'),
    url(r'^(\d+)/$', views.view_profile, name='view_profile'),
    url(r'^(\d+)/add_report$', views.add_report, name='add_report'),
]
