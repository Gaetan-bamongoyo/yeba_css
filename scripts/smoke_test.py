import json
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test import Client

client = Client()

home = client.get("/")
print("home", home.status_code)

game = client.get("/jeux/css-flexbox/")
print("game", game.status_code, b"game-levels" in game.content)

sync = client.post(
    "/api/progress/css-flexbox/",
    data=json.dumps(
        {"currentLevel": 2, "completedLevels": [0, 1], "isFinished": False}
    ),
    content_type="application/json",
)
print("sync", sync.status_code, sync.json())
