from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .models import Score
from .serializers import ScoreSerializer


class ScorePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ScoreViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing game scores/results.
    
    - List: GET /api/scores/ (with pagination)
    - Create: POST /api/scores/ (auto-calculates points and updates rating)
    - Retrieve: GET /api/scores/{id}/
    - Update: PATCH /api/scores/{id}/
    - Delete: DELETE /api/scores/{id}/ (recalculates player rating)
    
    Filtering:
    - ?game_id=value - filter by game
    - ?player_id=value - filter by player
    - ?result=win - filter by result (win, draw, loss)
    - ?ordering=-created_at - order by field
    """
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    pagination_class = ScorePagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['player__nickname', 'game__title', 'opponent_name']
    ordering_fields = ['created_at', 'points', 'result']
    ordering = ['-created_at']

    def get_queryset(self):
        """Apply additional filters."""
        queryset = super().get_queryset()
        
        game_id = self.request.query_params.get('game_id', None)
        if game_id:
            queryset = queryset.filter(game_id=game_id)
        
        player_id = self.request.query_params.get('player_id', None)
        if player_id:
            queryset = queryset.filter(player_id=player_id)
        
        result = self.request.query_params.get('result', None)
        if result in ['win', 'draw', 'loss']:
            queryset = queryset.filter(result=result)
        
        return queryset
