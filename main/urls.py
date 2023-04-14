from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("info/<str:id>/<str:title>", views.song_detail, name="song-detail"),
]
