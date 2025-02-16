from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>",views.display, name="display" ),
    path("search/",views.search, name="search"),
    path("new_entry/",views.new_entry,name="new_entry"),
    path("random_page/",views.random_page,name="random_page"),
    path("<str:title>/",views.edit_page,name="edit_page")
]
