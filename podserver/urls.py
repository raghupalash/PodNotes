from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("media/<str:query>", views.media, name="media"),
    path("currentPos", views.currentPos, name="currentPos"),
    path("addNote", views.addNote, name="addNote"),
    path("entries", views.entry, name="entry"),
    path("notes", views.getNotes, name="getNotes"),
    path("testNote", views.testNote),
]