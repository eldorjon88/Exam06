from django.db import models
from games.models import Game
from players.models import Player

RESULT_CHOICES = [
    ('win', 'Win'),
    ('draw', 'Draw'),
    ('loss', 'Loss'),
]

POINTS_MAP = {
    'win': 10,
    'draw': 5,
    'loss': 0,
}


class Score(models.Model):
    """Game score/result model."""
    id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    points = models.IntegerField(default=0)
    opponent_name = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('game', 'player')
        indexes = [
            models.Index(fields=['game']),
            models.Index(fields=['player']),
            models.Index(fields=['result']),
        ]

    def __str__(self):
        return f"{self.player.nickname} - {self.get_result_display()} ({self.points} pts)"

    def save(self, *args, **kwargs):
        """Auto-calculate points based on result."""
        self.points = POINTS_MAP.get(self.result, 0)
        super().save(*args, **kwargs)
