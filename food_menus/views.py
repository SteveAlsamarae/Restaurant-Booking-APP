from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView, DeleteView, CreateView, ListView

from .models import MenuModel
from .forms import MenuForm


class MenuListView(ListView):
    model = MenuModel
    context_object_name = "menus"
    template_name = "food_menus/menu_list.html"


class MenuCreateView(SuccessMessageMixin, CreateView):
    model = MenuModel
    form_class = MenuForm
    template_name = "food_menus/menu_create.html"
    success_message = "Menu created successfully"


class MenuUpdateView(SuccessMessageMixin, UpdateView):
    model = MenuModel
    form_class = MenuForm
    template_name = "food_menus/menu_update.html"
    success_message = "Menu updated successfully"


class MenuDeleteView(DeleteView):
    model = MenuModel
    template_name = "food_menus/menu_delete.html"
    success_url = "/"

    def get_success_url(self):
        messages.success(self.request, "Menu deleted successfully")
        return super().get_success_url()
