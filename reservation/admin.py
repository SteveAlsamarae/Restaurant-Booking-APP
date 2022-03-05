from django.contrib import admin

from .models import TableModel, RestaurantModel, ReservationModel


admin.site.register(RestaurantModel)
admin.site.register(TableModel)
admin.site.register(ReservationModel)
