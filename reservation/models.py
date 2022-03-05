from datetime import datetime, timedelta

from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
import uuid


RESTAURANT_HOURS = 9


class RestaurantModel(models.Model):
    name = models.CharField(max_length=200)
    opening_hour = models.TimeField()
    closing_hour = models.TimeField()
    email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def get_tables_for_a_date(self, date):
        return self.tables.filter(date=date)

    @property
    def get_available_tables(self):
        return self.tables.filter(is_available=True)


class TableModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey(
        RestaurantModel, on_delete=models.CASCADE, related_name="tables"
    )
    table_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_table_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Table #{self.number}"

    @property
    def get_table_number(self):
        return f"#{self.table_number}"


class ReservationModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    tables = models.ManyToManyField(TableModel, related_name="reservations")
    reservation_date = models.DateField(null=True)
    reservation_time = models.TimeField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def is_valid_date(self):
        return self.reservation_date >= timezone.now().date()

    class Meta:
        unique_together = ("customer", "reservation_date", "reservation_time")
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.customer.username}'s reservation"
