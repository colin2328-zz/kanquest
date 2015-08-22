from django.conf.urls import patterns, url

from .views import PlayerListView

urlpatterns = patterns(
    '',
    url(r'^players/$', PlayerListView.as_view(), name='players'),
)
