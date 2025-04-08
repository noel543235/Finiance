from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="resources"),
    path("images", views.images, name="images"),
    path("videos", views.videos, name="videos"),
    path("articles", views.articles, name="articles"),

]