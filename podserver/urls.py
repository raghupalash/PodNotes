from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("media/<str:query>", views.media, name="media"),
    path("currentPos", views.currentPos, name="currentPos"),
    path("addNote", views.note, name="addNote"),
    path("test", views.test),
    path("testNote", views.testNote),
]