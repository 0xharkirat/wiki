from django.urls import path

from . import views

app_name="wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("add", views.add, name="add"),
    path("random", views.random, name="random"),
    path("edit/<str:title>", views.edit, name="edit"),
]
