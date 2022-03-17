import imp
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from reservation.views import index_view, admin_login_view
from contact.views import contact_us_view


urlpatterns = [
    # core
    path("admin/", admin.site.urls),
    # 3rd parties
    path("accounts/", include("allauth.urls")),
    # local
    path("", index_view, name="index"),
    path("home/", index_view, name="home"),
    path("contact/", contact_us_view, name="contact_us"),
    path("radmin/login", admin_login_view, name="radmin_login"),
    path("profile/", include("users.urls")),
    path("food-menu/", include("food_menus.urls")),
    path("reservations/", include("reservation.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        urlpatterns += [
            path("__debug__/", include("debug_toolbar.urls")),
        ]
