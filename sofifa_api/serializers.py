from rest_framework import serializers
from .models import Sofifa

class GeneralSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('player_id', 'short_name', 'overall', 'age', 'value_eur',
                  'wage_eur','height_cm', 'weight_kg', 'league_name', 'club_name',
                  'club_position', 'nationality_name', 'player_face_url')
        model = Sofifa