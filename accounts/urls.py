from django.conf.urls import patterns, url
from django.contrib.auth.views import login
from django.contrib.auth.views import logout_then_login

from .views import home, RegisterView

urlpatterns = patterns(
    '',
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^$', home, name='home'),
)
