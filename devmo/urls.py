
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("publication/<int:publication_id>", views.publication, name="publication"),
    path("like/<int:publication_id>", views.like, name="like"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("profile/<str:username>/info", views.profile_info, name="profile_info"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("newpost", views.newpost, name="newpost"),
    path("category/<str:category>", views.category, name="category"),
    path("search", views.search, name="search"),
    path("favorites/<int:publication_id>", views.bookmark, name="bookmark"),
    path("favorites", views.view_favorites, name="view_favorites"),
]
