from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Game
from .serializers import GameSerializer


class GamePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class GameViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing games/tournaments.
    
    - List: GET /api/games/ (with pagination)
    - Create: POST /api/games/
    - Retrieve: GET /api/games/{id}/
    - Update: PATCH /api/games/{id}/
    - Delete: DELETE /api/games/{id}/ (protected if scores exist)
    
    Filtering:
    - ?search=title - search by title or location
    - ?ordering=start_date - order by field
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    pagination_class = GamePagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'location']
    ordering_fields = ['created_at', 'start_date', 'title']
    ordering = ['-created_at']

    def perform_destroy(self, instance):
        """Prevent deletion if game has scores."""
        if instance.score_set.exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Cannot delete game with associated scores.")
        instance.delete()
