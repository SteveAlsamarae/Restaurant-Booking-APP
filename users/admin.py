import imp
from django.contrib import admin
from django.contrib.auth.models import Group

from .models import UserProfile, RestaurantAdmin


admin.site.register(UserProfile)
admin.site.register(RestaurantAdmin)
admin.site.unregister(Group)
