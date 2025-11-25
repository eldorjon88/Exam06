from django.db import models


class Player(models.Model):
    """Chess player model."""
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=50, unique=True, blank=False)
    country = models.CharField(max_length=50, blank=True)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-rating', '-created_at']
        indexes = [
            models.Index(fields=['nickname']),
            models.Index(fields=['-rating']),
        ]

    def __str__(self):
        return self.nickname

    @property
    def total_games(self):
        """Calculate total games played."""
        return self.score_set.count()

    @property
    def wins(self):
        """Calculate total wins."""
        return self.score_set.filter(result='win').count()

    @property
    def draws(self):
        """Calculate total draws."""
        return self.score_set.filter(result='draw').count()

    @property
    def losses(self):
        """Calculate total losses."""
        return self.score_set.filter(result='loss').count()
