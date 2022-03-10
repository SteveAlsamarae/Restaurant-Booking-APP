from cProfile import label
from django import forms
from django.db import models

from crispy_forms.helper import FormHelper

from .models import MenuModel
from .models import FOOD_ITEM_VALIDATOR


class MenuForm(forms.ModelForm):
    name = forms.CharField(max_length=120, label="Item Name", help_text="i.e. Chicken Burger")
    food_items = forms.CharField(
        max_length=300,
        validators=[FOOD_ITEM_VALIDATOR],
        help_text="i.e. 'pizza, pasta, salad'",
    )

    class Meta:
        model = MenuModel
        fields = ["name", "menu_image", "price", "food_items"]

    def clean_food_items(self):
        food_items = self.cleaned_data.get("food_items")
        if food_items:
            food_items = food_items.lower()
        return food_items

    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
