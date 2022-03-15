from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import Message
from reservation.models import RestaurantModel


def contact_us_view(request):
    restaurant = RestaurantModel.objects.all()[0]

    if request.method == "POST":
        name = request.POST.get("name", None)
        email = request.POST.get("email", None)
        phone = request.POST.get("phone", None)
        message = request.POST.get("message", None)

        contact = Message.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message,
        )
        print(name, email, phone, message)
        contact.save()
        messages.success(request, "Your message has been submitted successfully.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    return render(request, "pages/contact_us.html", {"restaurant": restaurant})
