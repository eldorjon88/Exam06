from rest_framework import serializers


class LeaderboardSerializer(serializers.Serializer):
    """Serializer for leaderboard data."""
    rank = serializers.IntegerField()
    player_id = serializers.IntegerField()
    player_name = serializers.CharField()
    country = serializers.CharField()
    rating = serializers.IntegerField()
    points = serializers.IntegerField(required=False)
    total_games = serializers.IntegerField()
    wins = serializers.IntegerField()
    draws = serializers.IntegerField()
    losses = serializers.IntegerField()
