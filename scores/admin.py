from django.contrib import admin
from .models import Score


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'game', 'result', 'points', 'created_at')
    list_filter = ('result', 'created_at', 'game')
    search_fields = ('player__nickname', 'game__title', 'opponent_name')
    readonly_fields = ('points', 'created_at')
    fieldsets = (
        ('Score Information', {
            'fields': ('game', 'player', 'result', 'opponent_name', 'points')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
