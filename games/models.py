from django.db import models


class Game(models.Model):
    """Chess tournament/game model."""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=False)
    location = models.CharField(max_length=100, blank=False)
    start_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return self.title
