from rest_framework import serializers
from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    total_games = serializers.SerializerMethodField()
    wins = serializers.SerializerMethodField()
    draws = serializers.SerializerMethodField()
    losses = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['id', 'nickname', 'country', 'rating', 'total_games', 'wins', 'draws', 'losses', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_total_games(self, obj):
        return obj.total_games

    def get_wins(self, obj):
        return obj.wins

    def get_draws(self, obj):
        return obj.draws

    def get_losses(self, obj):
        return obj.losses
