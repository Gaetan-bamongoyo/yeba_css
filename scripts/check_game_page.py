import json
import os
import re

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test import Client

client = Client()
response = client.get("/jeux/css-flexbox/")
html = response.content.decode("utf-8")
print("status", response.status_code)

match = re.search(
    r'<script id="game-levels" type="application/json">(.*?)</script>',
    html,
    re.S,
)
print("levels script", bool(match))
if match:
    levels = json.loads(match.group(1))
    print("count", len(levels))
    print("title0", levels[0]["title"])
    print("has hint", "hint" in levels[0])
    print("has scene", "scene" in levels[0])

css = client.get("/static/css/style.css")
print("css status", css.status_code, "len", len(css.content))
print("css has page-enigma", b"page-enigma" in css.content)
print("css has game-area--enigma", b"game-area--enigma" in css.content)

engine = client.get("/static/js/games/flexbox/engine.js")
print("engine status", engine.status_code, "len", len(engine.content))
print("engine has revealHint", b"revealHint" in engine.content)
print("engine has Le site" , b"fant" in engine.content.lower() or b"RESOUDRE" in engine.content or b"R\xc3\x89SOUDRE" in engine.content)
