from django.urls import path

from .views import (
    add_admin_view,
    admin_logout_view,
    all_restaurant_admin_view,
    create_restaurant_view,
    update_resturant_view,
    add_table_view,
    update_table_view,
    delete_table_view,
    make_reservation_view,
    cancel_reservation_view,
    user_reservations_view,
    restaurant_admin_dashboard,
    todays_reservations_admin_view,
    upcoming_reservations_admin_view,
    past_reservations_admin_view,
    update_admin_view,
    delete_admin_view,

)


urlpatterns = [
    path("admin/add", add_admin_view, name="admin_add"),
    path("admin/<str:username>/update", update_admin_view, name="update_admin"),
    path("admin/<str:username>/delete", delete_admin_view, name="delete_admin"),
    path("admin/logout", admin_logout_view, name="admin_logout"),
    path("admins/", all_restaurant_admin_view, name="all_admins"),
    path("admin/dashboard", restaurant_admin_dashboard, name="admin_dashboard"),
    path("admin/todays/", todays_reservations_admin_view, name="todays_reservations"),
    path("admin/upcoming/", upcoming_reservations_admin_view, name="upcoming_reservations"),
    path("admin/past/", past_reservations_admin_view, name="past_reservations"),
    path("create-restaurant/", create_restaurant_view, name="create_restaurant"),
    path("update-restaurant/", update_resturant_view, name="update_restaurant"),
    path("add-table/", add_table_view, name="add_table"),
    path("update-table/<str:table_id>", update_table_view, name="update_table"),
    path("delete-table/<str:table_id>", delete_table_view, name="delete_table"),
    path("my-reservations/", user_reservations_view, name="user_reservations"),
    path("make_a_reservation/", make_reservation_view, name="make_reservation"),
    path("cancel_reservation/<str:reservation_id>/", cancel_reservation_view, name="cancel_reservation"),
]
