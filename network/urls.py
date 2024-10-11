
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following", views.following_page, name="following_page"),
    path("page/<int:PAGE>", views.paged_index, name="paged"),
    path("following/page/<int:PAGE>", views.paged_following, name="paged_following"),
    path("editpost", views.editpost, name="editpost"),
    path("like_fun", views.like_fun, name="like_fun"),
    path("access_profile/<str:username>", views.access_profile, name="access_profile")
]
