from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from catalog import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("a-propos/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("jeux/<slug:slug>/", views.game_play, name="game_play"),
    path("api/progress/<slug:slug>/", views.progress_sync, name="progress_sync"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
