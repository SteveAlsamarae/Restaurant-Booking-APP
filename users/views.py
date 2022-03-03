from xml.parsers.expat import model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import UserUpdateForm, UserProfileUpdateForm


def profile_update_view(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect("update_profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.profile)

    context = {
        "user": user_form,
        "profile": profile_form,
    }

    return render(request, "account/update_profile.html", context)
