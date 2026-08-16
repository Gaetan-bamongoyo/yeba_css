from django.contrib import admin

from .models import Game, Level


class LevelInline(admin.TabularInline):
    model = Level
    extra = 0
    fields = (
        "order",
        "title",
        "difficulty",
        "item_count",
        "is_active",
        "objective",
        "target_styles",
        "starter_code",
    )


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active", "order")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("title",)}
    fields = (
        "title",
        "slug",
        "short_description",
        "description",
        "cover_image",
        "is_active",
        "order",
    )
    inlines = [LevelInline]


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("title", "game", "order", "difficulty", "item_count", "is_active")
    list_filter = ("game", "difficulty", "is_active")
    search_fields = ("title", "objective")
