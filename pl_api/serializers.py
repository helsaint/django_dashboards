from rest_framework import serializers
from .models import PremierLeague

class PLSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('id', 'player', 'nation', 'pos', 'squad', 'age', 'born',
                  'avg_90s_played', 'sca', 'sca_per_90', 'pass_live', 'pass_dead',
                  'take_ons', 'shots', 'fld', 'sca_def', 'gca', 'gca_per_90', 'pass_live_goal',
                  'pass_dead_goal', 'to_goal', 'sh_goal', 'fld_goal', 'def_goal', 'unique_id')
        model = PremierLeague