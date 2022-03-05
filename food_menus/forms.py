from django import forms

from crispy_forms.helper import FormHelper

from .models import MenuModel


class MenuForm(forms.ModelForm):
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
