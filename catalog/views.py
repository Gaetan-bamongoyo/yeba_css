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
    levels = [level.as_pack_dict() for level in game.levels.filter(is_active=True)]
    progress = get_or_create_progress(request, game)

    context = {
        "game": game,
        "levels_pack": levels,
        "progress_pack": progress.as_dict(),
        "sync_url": reverse("progress_sync", kwargs={"slug": game.slug}),
    }
    return render(request, "games/flexbox.html", context)


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
