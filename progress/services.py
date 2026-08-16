from progress.models import GameProgress


def get_or_create_progress(request, game):
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    if request.user.is_authenticated:
        progress, _ = GameProgress.objects.get_or_create(
            game=game,
            user=request.user,
            defaults={"session_key": session_key},
        )
        return progress

    progress, _ = GameProgress.objects.get_or_create(
        game=game,
        session_key=session_key,
        user=None,
        defaults={},
    )
    return progress


def merge_progress_payload(progress, payload, level_count):
    current_level = int(payload.get("currentLevel", progress.current_level) or 0)
    completed = payload.get("completedLevels", progress.completed_levels) or []
    is_finished = bool(payload.get("isFinished", progress.is_finished))

    if current_level < 0:
        current_level = 0
    if level_count and current_level >= level_count:
        current_level = max(level_count - 1, 0)
        is_finished = True

    cleaned = []
    for value in completed:
        try:
            index = int(value)
        except (TypeError, ValueError):
            continue
        if 0 <= index < max(level_count, 1) and index not in cleaned:
            cleaned.append(index)

    # Keep the furthest progress (local or server).
    if current_level < progress.current_level:
        current_level = progress.current_level

    merged = sorted(set((progress.completed_levels or []) + cleaned))

    progress.current_level = current_level
    progress.completed_levels = merged
    progress.is_finished = is_finished or (
        level_count > 0 and len(merged) >= level_count
    )
    progress.save()
    return progress
