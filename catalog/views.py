import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_http_methods

from catalog.forms import ContactForm
from catalog.models import Game
from progress.services import get_or_create_progress, merge_progress_payload


@require_GET
def home(request):
    games = Game.objects.filter(is_active=True).prefetch_related("levels")
    return render(request, "catalog/home.html", {"games": games})


@require_GET
def about(request):
    return render(request, "catalog/about.html")


@require_http_methods(["GET", "POST"])
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Pour l'instant : confirmation locale. Brancher l'envoi email plus tard.
            messages.success(
                request,
                "Message envoyé ! Nous vous répondrons bientôt.",
            )
            return redirect("contact")
    else:
        form = ContactForm()

    return render(
        request,
        "catalog/contact.html",
        {
            "form": form,
            "contact_phone": "+243817675404",
            "contact_phone_display": "+243 817 675 404",
        },
    )

@require_GET
@ensure_csrf_cookie
def game_play(request, slug):
    game = get_object_or_404(Game, slug=slug, is_active=True)

    # SQL : d'abord la liste des enquêtes à choisir.
    if slug == "sql":
        from catalog.data.sql_registry import SQL_MISSIONS

        return render(
            request,
            "games/sql_hub.html",
            {
                "game": game,
                "missions": SQL_MISSIONS,
            },
        )

    levels_qs = game.levels.filter(is_active=True)
    if not levels_qs.exists():
        messages.info(request, "Ce jeu arrive bientôt.")
        return redirect("home")

    levels = [level.as_pack_dict() for level in levels_qs]
    progress = get_or_create_progress(request, game)

    context = {
        "game": game,
        "levels_pack": levels,
        "progress_pack": progress.as_dict(),
        "sync_url": reverse("progress_sync", kwargs={"slug": game.slug}),
    }
    return render(request, "games/flexbox.html", context)


@require_GET
@ensure_csrf_cookie
def game_mission(request, slug, mission):
    game = get_object_or_404(Game, slug=slug, is_active=True)

    if slug != "sql":
        return redirect("game_play", slug=slug)

    from catalog.data.sql_registry import get_sql_mission_pack

    pack = get_sql_mission_pack(mission)
    if not pack:
        messages.info(request, "Cette enquête n'existe pas encore.")
        return redirect("game_play", slug="sql")

    if not pack.get("is_playable"):
        messages.info(request, "Cette enquête arrive bientôt.")
        return redirect("game_play", slug="sql")

    # Progression isolée par mission (localStorage) — ne pas injecter
    # le GameProgress partagé du jeu "sql", sinon une mission pollue l'autre.
    mission_meta = {
        key: pack[key]
        for key in pack
        if key not in ("dataset", "levels")
    }
    empty_progress = {
        "currentLevel": 0,
        "completedLevels": [],
        "isFinished": False,
        "updatedAt": None,
    }

    return render(
        request,
        "games/sql.html",
        {
            "game": game,
            "mission": mission_meta,
            "levels_pack": pack["levels"],
            "progress_pack": empty_progress,
            "dataset_pack": pack["dataset"],
            "sync_url": "",
            "progress_slug": pack.get("progress_slug") or f"sql-mission-{mission}",
        },
    )


@require_http_methods(["GET", "POST"])
def progress_sync(request, slug):
    game = get_object_or_404(Game, slug=slug, is_active=True)
    progress = get_or_create_progress(request, game)

    if request.method == "GET":
        return JsonResponse(progress.as_dict())

    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON invalide"}, status=400)

    level_count = game.levels.filter(is_active=True).count()
    progress = merge_progress_payload(progress, payload, level_count)
    return JsonResponse(progress.as_dict())
