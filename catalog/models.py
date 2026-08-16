from django.db import models


class Game(models.Model):
    slug = models.SlugField(unique=True, max_length=80)
    title = models.CharField(max_length=120)
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(
        upload_to="games/covers/",
        blank=True,
        null=True,
        help_text="Image de couverture affichée sur la carte d'accueil.",
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    @property
    def cover_static_path(self):
        return f"img/games/{self.slug}.svg"

    def level_count(self):
        return self.levels.filter(is_active=True).count()


class Level(models.Model):
    game = models.ForeignKey(Game, related_name="levels", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=160)
    difficulty = models.CharField(max_length=40, default="Debutant")
    objective = models.TextField()
    item_count = models.PositiveIntegerField(default=1)
    target_styles = models.JSONField(default=dict)
    starter_code = models.TextField(default="#container {\n  display: flex;\n}")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        unique_together = [("game", "order")]

    def __str__(self):
        return f"{self.game.slug} #{self.order} — {self.title}"

    def as_pack_dict(self):
        return {
            "id": self.id,
            "order": self.order,
            "title": self.title,
            "difficulty": self.difficulty,
            "objective": self.objective,
            "itemCount": self.item_count,
            "target": self.target_styles,
            "starterCode": self.starter_code,
        }
