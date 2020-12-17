from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("create", views.create_view, name="create"),
    path("watch", views.watch_view, name="watch"),
    path("categories", views.categories_view, name="categories"),
    path("categories/<int:category_id>",
         views.category_list_view, name="category_list"),
    path("detail/<int:id>", views.detail_view, name="detail"),
    path("detail/<int:listing_id>/comment",
         views.comment_view, name="comment"),
    path("detail/<int:listing_id>/close", views.close_view, name="close")
]
