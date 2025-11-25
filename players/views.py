from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .models import Player
from .serializers import PlayerSerializer


class PlayerPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class PlayerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing players.
    
    - List: GET /api/players/ (with pagination)
    - Create: POST /api/players/
    - Retrieve: GET /api/players/{id}/
    - Update: PATCH /api/players/{id}/
    - Delete: DELETE /api/players/{id}/ (protected if scores exist)
    
    Filtering:
    - ?search=nickname - search by nickname
    - ?country=value - filter by country
    - ?min_rating=value - filter by minimum rating
    - ?ordering=-rating - order by field
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    pagination_class = PlayerPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nickname', 'country']
    ordering_fields = ['rating', 'created_at', 'nickname']
    ordering = ['-rating', '-created_at']

    def get_queryset(self):
        """Apply additional filters."""
        queryset = super().get_queryset()
        
        country = self.request.query_params.get('country', None)
        if country:
            queryset = queryset.filter(country__iexact=country)
        
        min_rating = self.request.query_params.get('min_rating', None)
        if min_rating:
            try:
                queryset = queryset.filter(rating__gte=int(min_rating))
            except ValueError:
                pass
        
        return queryset

    def perform_destroy(self, instance):
        """Prevent deletion if player has scores."""
        if instance.score_set.exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Cannot delete player with associated scores.")
        instance.delete()
