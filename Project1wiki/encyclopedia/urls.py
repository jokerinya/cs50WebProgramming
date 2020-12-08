from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/create", views.create, name="create"),
    path("wiki/random", views.random, name="random"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/<str:title>/edit", views.edit, name="edit")
]
