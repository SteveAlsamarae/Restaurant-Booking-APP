from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from .models import UserProfile, RestaurantAdmin
from .forms import RestaurantAdminForm


class UserProfileModelTest(TestCase):
    """Test User Profile Model is working properly"""

    def setUp(self) -> None:
        """Set up test environment for User Profile model"""

        self.user = User.objects.create_superuser(
            username="test", email="test@mail.com", password="test123"
        )
        self.client.force_login(self.user)
        UserProfile.objects.get_or_create(user=self.user)
        self.profile = UserProfile.objects.get(user__username="test")
        self.profile.name = "testuser"
        self.profile.phone_number = "01234567891"
        self.profile.save()

    def test_user_profile_model_creation(self):
        """user profile model should be created successfully"""

        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.name, "testuser")
        self.assertEqual(self.profile.phone_number, "01234567891")

    def test_user_profile_model_should_have_fields(self):
        """user profile model should have fields"""

        self.assertTrue(hasattr(self.profile, "user"))
        self.assertTrue(hasattr(self.profile, "name"))
        self.assertTrue(hasattr(self.profile, "phone_number"))
        self.assertFalse(hasattr(self.profile, "created_on"))

    def test_user_profile_model_should_have_str_method(self):
        """user profile model should have str method"""

        self.assertEqual(str(self.profile), "test's profile")

    def test_user_profile_model_should_have_delete_method(self):
        """user profile model should have delete_method to delete user profile"""

        profile = UserProfile.objects.get(user__username="test")
        self.assertEqual(hasattr(profile, "delete"), True)


class RestaurantAdminModelTest(TestCase):
    """Test Restaurant Admin Model is working properly"""

    def setUp(self) -> None:
        """Set up test environment for Restaurant Admin model"""

        self.user = User.objects.create_superuser(
            username="test", email="test@mail.com", password="test123"
        )
        self.client.force_login(self.user)
        RestaurantAdmin.objects.get_or_create(user=self.user)
        self.radmin = RestaurantAdmin.objects.get(user__username="test")
        self.radmin.name = "testuser"
        self.radmin.phone = "01234567891"
        self.radmin.role = "admin"
        self.radmin.is_active = True
        self.radmin.save()

    def test_restaurant_admin_model_creation(self):
        """user restaurant-admin model should be created successfully"""

        self.assertEqual(self.radmin.user, self.user)
        self.assertEqual(self.radmin.name, "testuser")
        self.assertEqual(self.radmin.phone, "01234567891")
        self.assertEqual(self.radmin.role, "admin")
        self.assertEqual(self.radmin.is_active, True)

    def test_restaurant_admin_model_should_have_fields(self):
        """user restaurant_admin model should have fields"""

        self.assertTrue(hasattr(self.radmin, "user"))
        self.assertTrue(hasattr(self.radmin, "name"))
        self.assertTrue(hasattr(self.radmin, "phone"))
        self.assertTrue(hasattr(self.radmin, "role"))
        self.assertTrue(hasattr(self.radmin, "is_active"))
        self.assertFalse(hasattr(self.radmin, "created_on"))

    def test_restaurant_admin_model_should_have_str_method(self):
        """user restaurant_admin model should have str method"""

        self.assertEqual(str(self.radmin), "test's restaurant admin")

    def test_restaurant_admin_should_have_properties(self):
        """user restaurant_admin model should have properties"""

        self.assertTrue(hasattr(self.radmin, "get_admin_avatar_url"))

    def test_restaurant_admin_model_should_have_delete_method(self):
        """user restaurant_admin model should have delete_method to delete user profile"""

        radmin = RestaurantAdmin.objects.get(user__username="test")
        self.assertEqual(hasattr(radmin, "delete"), True)


class RestaurantAdminFormTest(TestCase):
    """Test Restaurant Admin Form is working properly"""

    def test_restaurant_admin_form_should_have_fields(self):
        """restaurant admin form should have fields"""

        form = RestaurantAdminForm()
        self.assertTrue(form.fields["name"].required)
        self.assertTrue(form.fields["phone"].required)
        self.assertTrue(form.fields["role"].required)
        self.assertFalse(form.fields["is_active"].required)
        self.assertTrue(form.fields["avatar"].required)


class UserProfileUpdateViewTest(TestCase):
    """Test User Profile Update View is working properly"""

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(
            username="test", email="test@mail.com", password="test123"
        )
        self.client.force_login(self.user)

    def test_user_profile_update_view_should_return_200(self):
        """user profile update view should have fields"""

        response = self.client.get(reverse("update_profile"))
        self.assertEqual(response.status_code, 200)

    def test_user_profile_update_view_should_have_context(self):
        """user profile update view should have context"""

        response = self.client.get(reverse("update_profile"))
        self.assertIn("user_form", response.context)
        self.assertIn("profile_form", response.context)

    def test_user_profile_update_should_have_template(self):
        """user profile update should have template"""

        response = self.client.get(reverse("update_profile"))
        self.assertTemplateUsed(response, "account/update_profile.html")


class LoginTest(TestCase):
    """Test Login View is working properly"""

    def setUp(self) -> None:
        User.objects.create(username="test", email="test@mail.com", password="test123")

    def test_login_view_success(self):
        """login view should have fields"""

        response = self.client.post(
            "/accounts/login/", {"username": "test", "password": "test123"}
        )
        self.assertEqual(response.status_code, 200)


class SignupTest(TestCase):
    """Test Signup View is working properly"""

    def test_signup_view_should_redirect_upon_success(self):
        """signup view should have fields"""

        response = self.client.post(
            "/accounts/signup/",
            {
                "username": "test2",
                "email": "hi5@mail.com",
                "password1": "test1234",
                "password2": "test1234",
            },
        )

        self.assertEqual(response.status_code, 302)


class UserAppUrlsTest(TestCase):
    """Test User App Urls is working properly"""

    def test_user_app_urls_should_be_defined(self):
        """user app urls should have urls"""

        self.assertEqual(reverse("update_profile"), "/profile/update/")
