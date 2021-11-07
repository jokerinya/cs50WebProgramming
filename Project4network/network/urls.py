from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following_view, name="following"),

    # APIs
    path("post/<int:post_id>/like", views.post_like_view, name="post_like"),
]
