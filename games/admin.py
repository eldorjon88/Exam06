from django.contrib import admin
from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location', 'start_date', 'created_at')
    list_filter = ('start_date', 'created_at', 'location')
    search_fields = ('title', 'location', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Game Information', {
            'fields': ('title', 'location', 'start_date', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
