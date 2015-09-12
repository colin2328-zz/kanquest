from rest_framework.serializers import ModelSerializer

from game.models import Player


class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player
        fields = (
            'id', 'username', 'race_choice', 'num_population', 'num_mana',
            'num_units', 'num_acres', 'num_lumber', 'num_gold'
        )
