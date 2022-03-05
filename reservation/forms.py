from django import forms
from crispy_forms.helper import FormHelper

from .models import RestaurantModel, TableModel


class CreateRestaurantForm(forms.ModelForm):
    class Meta:
        model = RestaurantModel
        fields = ["name", "opening_hour", "closing_hour", "email", "contact_number"]

    def __init__(self, *args, **kwargs):
        super(CreateRestaurantForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False


class CreateTableForm(forms.ModelForm):
    class Meta:
        model = TableModel
        fields = ["restaurant", "table_number", "seats"]

    def clean_table_number(self):
        table_number = self.cleaned_data.get("table_number")
        if table_number:
            table_number = f"{str(table_number)}"
        return table_number

    def __init__(self, *args, **kwargs):
        super(CreateTableForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
