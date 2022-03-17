from django.test import TestCase
from django.shortcuts import reverse

from contact.models import Message
from reservation.models import RestaurantModel


class ContactModelTest(TestCase):
    """Test Contact-app models are working properly"""

    def setUp(self):
        """Set up test environment for Contact model"""

        Message.objects.create(
            name="Test Name",
            email="test@mail.com",
            phone="1234567890",
            message="Test message",
        )

    def test_contact_model_creation(self):
        """contact model should be created successfully"""

        msg = Message.objects.get(id=1)
        self.assertEqual(msg.name, "Test Name")
        self.assertEqual(msg.email, "test@mail.com")
        self.assertEqual(msg.phone, "1234567890")
        self.assertEqual(msg.message, "Test message")

    def test_contact_model_should_have_fields(self):
        """Contact model should have fields"""

        msg = Message()
        self.assertTrue(hasattr(msg, "name"))
        self.assertTrue(hasattr(msg, "email"))
        self.assertTrue(hasattr(msg, "phone"))
        self.assertTrue(hasattr(msg, "message"))

    def test_contact_model_has_str_method(self):
        """Contact model should have str method"""

        msg = Message.objects.get(id=1)
        self.assertTrue(hasattr(msg, "__str__"))
        self.assertTrue(str(msg), "Test Name - test@mail.com")


class ContactViewTest(TestCase):
    """Check if the Contact-app views are working properly"""

    def setUp(self):
        """Set up test environment for Contact model"""

        RestaurantModel.objects.create(
            name="Test Restaurant",
            opening_hour="10:00 AM",
            closing_hour="12:00 AM",
            contact_number="1234567890",
            email="test@mail.com",
        )

    def test_Contact_view_should_return_200(self):
        """Contact view should return 200"""

        response = self.client.get(reverse("contact_us"))
        self.assertEqual(response.status_code, 200)

    def test_Contact_view_should_have_template(self):
        """Contact view should have template"""

        response = self.client.get(reverse("contact_us"))
        self.assertTemplateUsed(response, "pages/contact_us.html")

    def test_contact_view_should_have_context(self):
        """Contact view should have context"""

        response = self.client.get(reverse("contact_us"))
        self.assertIn("restaurant", response.context)

    def test_restaurant_admin_view_requires_login(self):
        """restaurant admin view requires login"""

        response = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(response.status_code, 302)


class ContactUrlsTest(TestCase):
    """Check all the urls for Contact-app"""

    def test_reservation_urls_should_be_defined(self):
        """reservation urls should be defined"""

        self.assertEqual(reverse("contact_us"), "/contact/")
