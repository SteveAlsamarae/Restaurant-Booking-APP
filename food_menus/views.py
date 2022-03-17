from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, user_passes_test

from reservation.views import is_radmin_check
from .models import MenuModel
from .forms import MenuForm


class MenuListView(ListView):
    """Index page food menus

    - List all food menus
    - Show menu price
    - Customer can view food menu
    """
    model = MenuModel
    context_object_name = "menus"
    template_name = "food_menus/menu_list.html"


# ===============================
# Admin manage restaurant menu
# ===============================
@login_required
@user_passes_test(is_radmin_check)
def radmin_foodmenu_view(request):
    form = MenuForm()
    menus = MenuModel.objects.all()

    context = {
        "form": form,
        "menus": menus,
    }

    return render(request, "food_menus/radmin_foodmenu.html", context)


@login_required
@user_passes_test(is_radmin_check)
def add_food_item_view(request):
    if request.method == "POST":
        form = MenuForm(
            request.POST,
            request.FILES,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Menu added successfully")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, f"Errors: {form.errors}")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
@user_passes_test(is_radmin_check)
def update_menu_view(request, menu_id):
    menu = get_object_or_404(MenuModel, id=menu_id)
    if request.method == "POST":
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.save()
            messages.success(
                request,
                f"{menu.name} is updated successfully",
            )
            return redirect("admin_menu_list")
    else:
        form = MenuForm(instance=menu)
    return render(request, "food_menus/menu_update.html", {"form": form})


@login_required
@user_passes_test(is_radmin_check)
def delete_menu_view(request, menu_id):
    menu = get_object_or_404(MenuModel, id=menu_id)
    menu.delete()
    messages.success(request, f"{menu.name} is deleted successfully")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
