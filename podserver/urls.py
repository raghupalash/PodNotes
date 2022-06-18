from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/<str:query>", views.search, name="search"),
    path("media/<str:query>", views.media, name="media"),
]