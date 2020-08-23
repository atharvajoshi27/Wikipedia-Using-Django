from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("createnew/", views.createnew, name='wiki-createnew'),
    path("randompage/", views.randompage, name='wiki-random'),
    path("wikisearch/", views.wikisearch, name='wiki-search'),
    path("wikiedit/<str:title>", views.wikiedit, name='wiki-edit'),
    path("wiki/<str:title>", views.wiki, name="wiki"),
]
