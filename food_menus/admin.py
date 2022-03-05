from django.contrib import admin

from .models import MenuModel


class MenuAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]
    search_fields = ["name"]
    ordering = ["-created_on"]


# Register menu model to admin panel.
admin.site.register(MenuModel, MenuAdmin)
