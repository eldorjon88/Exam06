from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count, Sum, F, Case, When, IntegerField
from games.models import Game
from players.models import Player
from scores.models import Score
from .serializers import LeaderboardSerializer


class LeaderboardPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class LeaderboardViewSet(viewsets.ViewSet):
    """
    ViewSet for leaderboards (no update/delete operations).
    
    - GET /api/leaderboard/?game_id={id} - leaderboard for a specific game
    - GET /api/leaderboard/top/?game_id={id}&limit={n} - top N players in a game
    - GET /api/leaderboard/global/?country={country}&limit={n} - global player ratings
    """
    pagination_class = LeaderboardPagination

    def list(self, request, *args, **kwargs):
        """List leaderboard for a game (sort by points desc)."""
        game_id = request.query_params.get('game_id', None)
        
        if not game_id:
            return Response(
                {'error': 'game_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response(
                {'error': 'Game not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        scores = Score.objects.filter(game=game).select_related('player').order_by('-points')
        
        leaderboard_data = []
        for rank, score in enumerate(scores, 1):
            leaderboard_data.append({
                'rank': rank,
                'player_id': score.player.id,
                'player_name': score.player.nickname,
                'country': score.player.country,
                'rating': score.player.rating,
                'points': score.points,
                'wins': score.player.wins,
                'draws': score.player.draws,
                'losses': score.player.losses,
            })
        
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(leaderboard_data, request)
        if page is not None:
            return paginator.get_paginated_response(page)
        
        return Response(leaderboard_data)

    @action(detail=False, methods=['get'])
    def top(self, request, *args, **kwargs):
        """Get top N players in a specific game."""
        game_id = request.query_params.get('game_id', None)
        limit = request.query_params.get('limit', 10)
        
        if not game_id:
            return Response(
                {'error': 'game_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            game = Game.objects.get(id=game_id)
            limit = int(limit)
        except Game.DoesNotExist:
            return Response(
                {'error': 'Game not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {'error': 'limit must be an integer'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        scores = Score.objects.filter(game=game).select_related('player').order_by('-points')[:limit]
        
        leaderboard_data = []
        for rank, score in enumerate(scores, 1):
            leaderboard_data.append({
                'rank': rank,
                'player_id': score.player.id,
                'player_name': score.player.nickname,
                'country': score.player.country,
                'rating': score.player.rating,
                'points': score.points,
                'wins': score.player.wins,
                'draws': score.player.draws,
                'losses': score.player.losses,
            })
        
        return Response(leaderboard_data)

    @action(detail=False, methods=['get'])
    def global_leaderboard(self, request, *args, **kwargs):
        """Get global player ratings leaderboard."""
        country = request.query_params.get('country', None)
        limit = request.query_params.get('limit', 50)
        
        try:
            limit = int(limit)
        except ValueError:
            return Response(
                {'error': 'limit must be an integer'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        players = Player.objects.all().order_by('-rating')
        
        if country:
            players = players.filter(country__iexact=country)
        
        players = players[:limit]
        
        leaderboard_data = []
        for rank, player in enumerate(players, 1):
            leaderboard_data.append({
                'rank': rank,
                'player_id': player.id,
                'player_name': player.nickname,
                'country': player.country,
                'rating': player.rating,
                'total_games': player.total_games,
                'wins': player.wins,
                'draws': player.draws,
                'losses': player.losses,
            })
        
        return Response(leaderboard_data)
