from django.conf.urls import patterns, url

from .views import PlayerListView, PlayerDetailView

urlpatterns = patterns(
    '',
    url(r'^players/$', PlayerListView.as_view(), name='player_list'),
    url(r'^players/(?P<pk>[0-9]+)/$', PlayerDetailView.as_view(), name='player_detail'),
)
