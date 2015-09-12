from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from game.models import Player
from .serializers import PlayerSerializer


class PlayerViewSet(ReadOnlyModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    @detail_route(methods=['post'])
    def action(self, request, pk=None):
        player = self.get_object()
        action = request.data.get('action')
        # import ipdb; ipdb.set_trace()
        return Response(request.data)
