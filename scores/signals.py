from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Score
from players.models import Player


@receiver(post_save, sender=Score)
def update_player_rating_on_score_save(sender, instance, created, **kwargs):
    """Update player rating when a score is created or modified."""
    player = instance.player
    
    total_points = player.score_set.aggregate(total=Sum('points'))['total'] or 0
    
    new_rating = 1000 + (total_points // 2)
    
    if player.rating != new_rating:
        player.rating = new_rating
        player.save(update_fields=['rating'])


@receiver(post_delete, sender=Score)
def update_player_rating_on_score_delete(sender, instance, **kwargs):
    """Update player rating when a score is deleted."""
    player = instance.player
    
    total_points = player.score_set.aggregate(total=Sum('points'))['total'] or 0
    new_rating = 1000 + (total_points // 2)
    
    if player.rating != new_rating:
        player.rating = new_rating
        player.save(update_fields=['rating'])
