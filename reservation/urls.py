from django.urls import path

from .views import (
    create_restaurant_view,
    update_resturant_view,
    add_table_view,
    update_table_view,
    delete_table_view,
    make_reservation_view,
    update_reservation_view,
    delete_reservation_view,
    check_duplicate_reservation,
)

# TODO: Add urls later

urlpatterns = [
    path("make_a_reservation/", make_reservation_view, name="make_reservation"),
    path(
        "delete_reservation/<int:reservation_id>/",
        delete_reservation_view,
        name="delete_reservation",
    ),
]
