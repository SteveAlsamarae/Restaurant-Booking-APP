from django.urls import path

from .views import (
    MenuCreateView,
    MenuDeleteView,
    MenuListView,
    MenuUpdateView,
)

urlpatterns = [
    path("all/", MenuListView.as_view(), name="menu_list"),
    path("create/", MenuCreateView.as_view(), name="menu_create"),
    path("<str:pk>/update/", MenuUpdateView.as_view(), name="menu_update"),
    path("<str:pk>/delete/", MenuDeleteView.as_view(), name="menu_delete"),
]
