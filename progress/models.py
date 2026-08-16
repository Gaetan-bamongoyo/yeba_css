from django.conf import settings
from django.db import models

from catalog.models import Game


class GameProgress(models.Model):
    game = models.ForeignKey(Game, related_name="progress_entries", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="game_progress",
        on_delete=models.CASCADE,
    )
    session_key = models.CharField(max_length=40, blank=True, db_index=True)
    current_level = models.PositiveIntegerField(default=0)
    completed_levels = models.JSONField(default=list, blank=True)
    is_finished = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "game progress"
        constraints = [
            models.UniqueConstraint(
                fields=["game", "user"],
                condition=models.Q(user__isnull=False),
                name="uniq_progress_game_user",
            ),
            models.UniqueConstraint(
                fields=["game", "session_key"],
                condition=models.Q(user__isnull=True) & ~models.Q(session_key=""),
                name="uniq_progress_game_session",
            ),
        ]

    def __str__(self):
        owner = self.user or self.session_key or "anon"
        return f"{self.game.slug} — {owner} @ {self.current_level}"

    def as_dict(self):
        return {
            "currentLevel": self.current_level,
            "completedLevels": self.completed_levels or [],
            "isFinished": self.is_finished,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }
