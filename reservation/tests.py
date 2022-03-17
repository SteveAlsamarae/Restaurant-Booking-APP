from django.shortcuts import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.dateparse import parse_time
import datetime

from django.utils import timezone

from .models import RestaurantModel, TableModel, ReservationModel
from .forms import CreateRestaurantForm, CreateTableForm


class ReservationModelTest(TestCase):
    """Test reservation-app models are working properly"""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="test123",
            email="test123@mail.com",
            password="test123",
        )
        self.client.force_login(self.user)

        RestaurantModel.objects.create(
            name="test_restaurant",
            opening_hour="12:00",
            closing_hour="19:00",
            contact_number="01234567891",
            email="test@mail.com",
        )
        self.restaurant = RestaurantModel.objects.get(name="test_restaurant")
        TableModel.objects.create(
            restaurant=RestaurantModel.objects.get(name="test_restaurant"),
            table_number=1,
            seats=4,
        )
        self.table = TableModel.objects.get(table_number=1)
        ReservationModel.objects.create(
            customer=self.user,
            table=self.table,
            reservation_time=parse_time("12:00"),
            message="test message",
            reservation_date=datetime.datetime.strptime(
                "11/15/2022", "%m/%d/%Y"
            ).date(),
        )
        self.reservation = ReservationModel.objects.get(table__table_number=1)

    def test_restaurant_model_creation(self):
        """restaurant model should be created successfully"""

        restaurant = RestaurantModel.objects.get(name="test_restaurant")
        self.assertEqual(restaurant.name, "test_restaurant")
        self.assertEqual(restaurant.opening_hour, parse_time("12:00"))
        self.assertEqual(restaurant.closing_hour, parse_time("19:00"))
        self.assertEqual(restaurant.contact_number, "01234567891")
        self.assertEqual(restaurant.email, "test@mail.com")

    def test_table_model_creation(self):
        """table model should be created successfully"""

        table = TableModel.objects.get(table_number=1)
        self.assertEqual(table.table_number, 1)
        self.assertEqual(table.seats, 4)
        self.assertEqual(table.restaurant.name, "test_restaurant")

    def test_reservation_model_creation(self):
        """reservation model should be created successfully"""

        self.assertEqual(self.reservation.customer, self.user)
        self.assertEqual(self.reservation.table, self.table)
        self.assertEqual(self.reservation.reservation_time, parse_time("12:00"))
        self.assertEqual(self.reservation.message, "test message")
        self.assertEqual(
            self.reservation.reservation_date,
            datetime.datetime.strptime("11/15/2022", "%m/%d/%Y").date(),
        )

    def test_restaurant_model_should_have_fields(self):
        """restaurant model should have fields"""

        restaurant = RestaurantModel()
        self.assertTrue(hasattr(restaurant, "name"))
        self.assertTrue(hasattr(restaurant, "opening_hour"))
        self.assertTrue(hasattr(restaurant, "closing_hour"))
        self.assertTrue(hasattr(restaurant, "contact_number"))
        self.assertTrue(hasattr(restaurant, "email"))

    def test_table_model_should_have_fields(self):
        """table  model should have fields"""

        self.assertTrue(hasattr(self.table, "restaurant"))
        self.assertTrue(hasattr(self.table, "table_number"))
        self.assertTrue(hasattr(self.table, "seats"))

    def test_reservation_model_should_have_fields(self):
        """reservation model should have fields"""

        self.assertTrue(hasattr(self.reservation, "reservation_date"))
        self.assertTrue(hasattr(self.reservation, "reservation_time"))
        self.assertTrue(hasattr(self.reservation, "message"))
        self.assertTrue(hasattr(self.reservation, "customer"))
        self.assertTrue(hasattr(self.reservation, "table"))

    def test_restaurant_model_should_have_str_method(self):
        """restaurant model should have str method"""

        self.assertEqual(str(self.restaurant), "test_restaurant")

    def test_table_model_should_have_str_method(self):
        """table model should have str method"""

        self.assertEqual(str(self.table), "Table #1")

    def test_table_model_should_have_properties(self):
        """table model should have defined properties"""

        self.assertTrue(hasattr(self.table, "get_table_number"))

    def test_reservation_model_should_have_str_method(self):
        """reservation model should have str method"""

        self.assertEqual(
            str(self.reservation),
            "test123's reservation for #1",
        )

    def test_reservation_model_should_have_methods(self):
        """reservation model should have defined methods"""

        self.assertTrue(hasattr(self.reservation, "is_valid_date"))


class ReservationModelFormTest(TestCase):
    """Check if the reservation-app forms are valid or not"""

    def test_create_restaurant_form_should_have_required_fields(self):
        """create restaurant form should have required fields"""

        form = CreateRestaurantForm()
        self.assertTrue(form.fields["name"].required)
        self.assertTrue(form.fields["opening_hour"].required)
        self.assertTrue(form.fields["closing_hour"].required)
        self.assertFalse(form.fields["contact_number"].required)
        self.assertFalse(form.fields["email"].required)

    def test_create_restaurant_form_valid(self):
        """create restaurant form should be valid"""

        form = CreateRestaurantForm(
            data={
                "name": "test_restaurant",
                "opening_hour": "12:00",
                "closing_hour": "19:00",
                "contact_number": "01234567891",
                "email": "test@mail.com",
            }
        )
        self.assertTrue(form.is_valid())

    def test_create_table_form_should_have_required_fields(self):
        """create restaurant form should have required fields"""

        form = CreateTableForm()
        self.assertTrue(form.fields["table_number"].required)
        self.assertTrue(form.fields["seats"].required)

    def test_create_table_form_valid(self):
        """create restaurant form should be valid"""

        form = CreateTableForm(data={"table_number": 1, "seats": 4})
        self.assertTrue(form.is_valid())

    def test_create_table_should_have_clean_method(self):
        """create restaurant form should have clean method"""

        form = CreateTableForm()
        self.assertTrue(hasattr(form, "clean_table_number"))


class ReservationViewTest(TestCase):
    """Check if the reservation-app views are working properly"""

    def setUp(self):
        User.objects.create_superuser(
            username="test123",
            email="test123@mail.com",
            password="test123",
        )
        self.user = User.objects.get(username="test123")
        self.client.force_login(self.user)

        RestaurantModel.objects.create(
            name="test_restaurant",
            opening_hour="12:00",
            closing_hour="19:00",
            contact_number="01234567891",
            email="test@mail.com",
        )
        self.restaurant = RestaurantModel.objects.get(name="test_restaurant")
        TableModel.objects.create(
            restaurant=self.restaurant,
            table_number=1,
            seats=4,
        )
        self.table = TableModel.objects.get(table_number=1)

    def test_index_view(self):
        """index view should return 200"""

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_view(self):
        """home page view should return 200"""

        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)

    def test_index_page_use_template(self):
        """index page should use template"""

        response = self.client.get("/")
        self.assertTemplateUsed(response, "pages/index.html")

    def test_make_reservation_view_should_return_200(self):
        """reservation view should return 200"""

        response = self.client.get(reverse("make_reservation"))
        self.assertEqual(response.status_code, 200)

    def test_make_reservation_view_should_have_template(self):
        """reservation view should have template"""

        response = self.client.get(reverse("make_reservation"))
        self.assertTemplateUsed(response, "reservation/make_reservation.html")

    def test_make_reservation_view_should_have_context(self):
        """reservation view should have context"""

        response = self.client.get(reverse("make_reservation"))
        self.assertIn("restaurant", response.context)
        self.assertIn("tables", response.context)
        self.assertIn("available_times", response.context)

    def test_admin_login_view_should_return_200(self):
        """admin login view should return 200"""

        response = self.client.get(reverse("radmin_login"))
        self.assertEqual(response.status_code, 200)

    def test_admin_login_view_should_have_template(self):
        """admin login view should have template"""

        response = self.client.get(reverse("radmin_login"))
        self.assertTemplateUsed(response, "restaurant_admin/login_admin.html")

    def test_admin_login_view_should_have_form(self):
        """admin login view should have form"""

        response = self.client.get(reverse("radmin_login"))
        self.assertIn("form", response.context)

    def test_radmin_post_request(self):
        """radmin post request should return 302"""

        response = self.client.post(
            reverse("radmin_login"),
            data={"username": "test123", "password": "test123"},
        )
        self.assertEqual(response.status_code, 302)

    def test_radmin_redirect_url(self):
        """radmin redirect url should be admin_dashboard"""

        response = self.client.post(
            reverse("radmin_login"),
            data={"username": "test123", "password": "test123"},
        )
        self.assertRedirects(response, reverse("admin_dashboard"))

    def test_admin_dashboard_view_should_return_200(self):
        """admin dashboard view should return 200"""

        response = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_view_should_have_template(self):
        """admin dashboard view should have template"""

        response = self.client.get(reverse("admin_dashboard"))
        self.assertTemplateUsed(response, "restaurant_admin/dashboard.html")

    def test_admin_dashboard_view_should_have_context(self):
        """admin dashboard view should have context"""

        response = self.client.get(reverse("admin_dashboard"))
        self.assertIn("restaurant", response.context)
        self.assertIn("tables", response.context)
        self.assertIn("tables_n_reservation", response.context)
        self.assertIn("form", response.context)

    def test_todays_reservations_view(self):
        """todays reservations view should return 200"""

        response = self.client.get(reverse("todays_reservations"))
        self.assertEqual(response.status_code, 200)

    def test_todays_reservations_view_should_have_template(self):
        """todays reservations view should have template"""

        response = self.client.get(reverse("todays_reservations"))
        self.assertTemplateUsed(response, "restaurant_admin/todays.html")

    def test_todays_reservations_view_should_have_context(self):
        """todays reservations view should have context"""

        response = self.client.get(reverse("todays_reservations"))
        self.assertIn("reservations", response.context)

    def test_upcoming_reservations_view(self):
        """upcoming reservations view should return 200"""

        response = self.client.get(reverse("upcoming_reservations"))
        self.assertEqual(response.status_code, 200)

    def test_upcoming_reservations_view_should_have_template(self):
        """upcoming reservations view should have template"""

        response = self.client.get(reverse("upcoming_reservations"))
        self.assertTemplateUsed(response, "restaurant_admin/upcoming_reservations.html")

    def test_upcoming_reservations_view_should_have_context(self):
        """upcoming reservations view should have context"""

        response = self.client.get(reverse("upcoming_reservations"))
        self.assertIn("reservations", response.context)

    def test_past_reservations_view(self):
        """past reservations view should return 200"""

        response = self.client.get(reverse("past_reservations"))
        self.assertEqual(response.status_code, 200)

    def test_past_reservations_view_should_have_template(self):
        """past reservations view should have template"""

        response = self.client.get(reverse("past_reservations"))
        self.assertTemplateUsed(response, "restaurant_admin/past_reservations.html")

    def test_past_reservations_view_should_have_context(self):
        """past reservations view should have context"""

        response = self.client.get(reverse("past_reservations"))
        self.assertIn("reservations", response.context)

    def test_create_restaurant_view(self):
        """create restaurant view should return 302"""

        response = self.client.get(reverse("create_restaurant"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("admin_dashboard"))

    def test_update_restaurant_view(self):
        """update restaurant view should return 200"""

        response = self.client.get(reverse("update_restaurant"))
        self.assertEqual(response.status_code, 200)

    def test_update_restaurant_view_should_have_template(self):
        """update restaurant view should have template"""

        response = self.client.get(reverse("update_restaurant"))
        self.assertTemplateUsed(response, "restaurant_admin/update_restaurant.html")

    def test_update_restaurant_post_view(self):
        """update restaurant post view should return 302"""

        response = self.client.post(
            reverse("update_restaurant"),
            data={"name": "test", "opening_hour": "10:00", "closing_hour": "20:00"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("admin_dashboard"))
        restaurant = RestaurantModel.objects.get(name="test")
        self.assertEqual(restaurant.name, "test")

    def test_update_table_view(self):
        """update table view should return 200"""

        response = self.client.get(
            reverse(
                "update_table",
                kwargs={"table_id": self.table.id},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_update_table_view_should_have_template(self):
        """update table view should have template"""

        response = self.client.get(
            reverse(
                "update_table",
                kwargs={"table_id": self.table.id},
            )
        )
        self.assertTemplateUsed(response, "restaurant_admin/update_table.html")

    def test_update_table_post_view(self):
        """update table post view should return 302"""

        response = self.client.post(
            reverse("update_table", kwargs={"table_id": self.table.id}),
            data={"table_number": "2", "seats": "10"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("admin_dashboard"))
        table = TableModel.objects.get(table_number=2)
        self.assertEqual(table.seats, 10)

    def test_delete_table_view(self):
        """delete table view should return 302"""

        TableModel.objects.create(
            restaurant=self.restaurant,
            table_number=3,
            seats=6,
        )
        table = TableModel.objects.get(table_number=3)
        response = self.client.get(
            reverse(
                "delete_table",
                kwargs={"table_id": table.id},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TableModel.objects.filter(id=table.id).exists())

    def test_cancel_reservation_view(self):
        """cancel reservation view should return 302"""
        ReservationModel.objects.create(
            table=self.table,
            customer=self.user,
            reservation_date=timezone.now().date(),
            reservation_time=timezone.now().time(),
            message="test message",
        )
        reservation = ReservationModel.objects.get(table__table_number=1)
        response = self.client.get(
            reverse(
                "cancel_reservation",
                kwargs={"reservation_id": reservation.id},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ReservationModel.objects.filter(id=reservation.id).exists())

    def test_admin_dashboard_view_requires_login(self):
        """admin dashboard view should required login"""

        self.client.logout()
        response = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(response.status_code, 302)


class ReservationUrlsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="testuser", email="testuser@mail.com", password="testpassword"
        )
        self.client.force_login(self.user)

    def test_reservation_urls_should_be_defined(self):
        """reservation urls should be defined"""

        self.assertEqual(reverse("user_reservations"), "/reservations/my-reservations/")
        self.assertEqual(reverse("admin_add"), "/reservations/admin/add")
        self.assertEqual(reverse("todays_reservations"), "/reservations/admin/todays/")
        self.assertEqual(reverse("upcoming_reservations"), "/reservations/admin/upcoming/")
        self.assertEqual(reverse("past_reservations"), "/reservations/admin/past/")
