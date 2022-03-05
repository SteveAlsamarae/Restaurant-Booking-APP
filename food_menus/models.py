import uuid
from django.db import models
from django.shortcuts import reverse
from django.core.validators import RegexValidator

from django_resized import ResizedImageField


FOOD_ITEM_VALIDATOR = RegexValidator(
    r"^[, a-zA-Z]*$", "Enter comma separated items. (use space to seperate two items)"
)


class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu_image = ResizedImageField(
        size=[400, 500],
        upload_to="menu_images/",
        crop=["middle", "center"],
        quality=80,
        keep_meta=False,
        force_format="JPEG",
    )
    name = models.CharField(max_length=120)
    food_items = models.CharField(max_length=300, validators=[FOOD_ITEM_VALIDATOR])
    price = models.IntegerField(max_length=10, verbose_name="Price")
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.food_items:
            self.food_items = self.food_items.lower()
        super(Menu, self).save(*args, **kwargs)

    # delete menu image too when menu is deleted
    def delete(self, *args, **kwargs):
        self.menu_image.delete()
        super(Menu, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("food-menu", kwargs={"id": self.id})

    @property
    def get_comma_seperated_food_items(self):
        return self.food_items.split(",")

    @property
    def get_menu_image_url(self):
        return self.menu_image.url

    @property
    def get_price_in_dollars(self):
        return f"${self.price}"
