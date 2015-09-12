from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from game.models import Player
from game.exceptions import GameException
from .serializers import PlayerSerializer
from .actions import Action


class PlayerViewSet(ReadOnlyModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    @detail_route(methods=['post'])
    def action(self, request, pk=None):
        player = self.get_object()
        action = request.data.get('action')
        try:
            result = getattr(Action(player, request.data), action)()
        except GameException as e:
            return Response({'message': e.message}, status=HTTP_400_BAD_REQUEST)
        return Response({'message': result if result else ''}, status=HTTP_200_OK)
