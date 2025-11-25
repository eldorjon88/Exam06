from rest_framework import serializers
from .models import Score, POINTS_MAP


class ScoreSerializer(serializers.ModelSerializer):
    result_display = serializers.CharField(source='get_result_display', read_only=True)
    player_nickname = serializers.CharField(source='player.nickname', read_only=True)
    game_title = serializers.CharField(source='game.title', read_only=True)

    class Meta:
        model = Score
        fields = ['id', 'game', 'game_title', 'player', 'player_nickname', 'result', 
                  'result_display', 'points', 'opponent_name', 'created_at']
        read_only_fields = ['id', 'points', 'created_at']

    def create(self, validated_data):
        """Auto-set points based on result."""
        result = validated_data.get('result')
        validated_data['points'] = POINTS_MAP.get(result, 0)
        return super().create(validated_data)
