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
    path("<int:id>/update/", MenuUpdateView.as_view(), name="menu_update"),
    path("<int:id>/delete/", MenuDeleteView.as_view(), name="menu_delete"),
]
