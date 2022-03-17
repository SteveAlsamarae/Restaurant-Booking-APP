from django.urls import path

from .views import (
    radmin_foodmenu_view,
    add_food_item_view,
    update_menu_view,
    delete_menu_view,
    MenuListView,
)

urlpatterns = [
    path("all/", MenuListView.as_view(), name="menu_list"),
    path("admin/", radmin_foodmenu_view, name="admin_menu_list"),
    path("create/", add_food_item_view, name="menu_create"),
    path("<str:menu_id>/update/", update_menu_view, name="menu_update"),
    path("<str:menu_id>/delete/", delete_menu_view, name="menu_delete"),
]
