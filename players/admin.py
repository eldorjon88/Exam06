from django.contrib import admin
from .models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'country', 'rating', 'total_games', 'created_at')
    list_filter = ('country', 'created_at')
    search_fields = ('nickname', 'country')
    readonly_fields = ('created_at', 'total_games', 'wins', 'draws', 'losses')
    fieldsets = (
        ('Player Information', {
            'fields': ('nickname', 'country', 'rating')
        }),
        ('Statistics', {
            'fields': ('total_games', 'wins', 'draws', 'losses'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def total_games(self, obj):
        return obj.total_games
    total_games.short_description = 'Total Games'

    def wins(self, obj):
        return obj.wins
    wins.short_description = 'Wins'

    def draws(self, obj):
        return obj.draws
    draws.short_description = 'Draws'

    def losses(self, obj):
        return obj.losses
    losses.short_description = 'Losses'
