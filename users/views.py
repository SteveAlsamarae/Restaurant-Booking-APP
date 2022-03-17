from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import RestaurantAdmin
from .forms import UserUpdateForm, UserProfileUpdateForm, RestaurantAdminForm


@login_required
def profile_update_view(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("update_profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, "account/update_profile.html", context)


@login_required
def add_restaurant_admin(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = RestaurantAdminForm(request.POST)
        if form.is_valid():
            restaurant_admin = form.save(commit=False)
            restaurant_admin.user = user
            restaurant_admin.save()
            messages.success(request, "Restaurant admin added successfully.")
            return redirect("update_profile")


@login_required
def update_restaurant_admin(request, id):
    restaurant_admin = RestaurantAdmin.objects.get(id=id)

    if request.method == "POST":
        form = RestaurantAdminForm(request.POST, instance=restaurant_admin)
        if form.is_valid():
            restaurant_admin = form.save(commit=False)
            restaurant_admin.save()
            messages.success(request, "Restaurant admin added successfully.")
            return redirect("update_profile")
    else:
        form = RestaurantAdminForm(instance=restaurant_admin)
