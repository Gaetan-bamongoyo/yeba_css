from django.contrib import admin

from .models import GameProgress


@admin.register(GameProgress)
class GameProgressAdmin(admin.ModelAdmin):
    list_display = ("game", "user", "session_key", "current_level", "is_finished", "updated_at")
    list_filter = ("game", "is_finished")
    search_fields = ("session_key", "user__username")
