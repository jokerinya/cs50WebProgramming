from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following_view, name="following"),
    path("profile", views.profile_view, name="profile"),


    # APIs
    path("post/<int:post_id>/edit", views.post_edit_view, name="post_edit"),
    path("user/<int:user_id>/follow", views.user_follow_view, name="user_follow"),
]
