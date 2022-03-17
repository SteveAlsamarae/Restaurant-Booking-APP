from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import MenuModel
from .forms import MenuForm


class MenuModelTest(TestCase):
    """Test Food Menu Model is working properly"""

    def setUp(self) -> None:
        MenuModel.objects.create(
            name="menu1", food_items="test, test2, test3", price=10
        )
        MenuModel.objects.create(
            name="menu2", food_items="item_a, item_b, item_c", price=20
        )
        MenuModel.objects.create(
            name="menu3", food_items="item_x, item_y, item_z", price=30
        )

    def test_menu_model_creation(self):
        """menu model should be created successfully"""

        menu = MenuModel.objects.get(name="menu1")

        self.assertEqual(menu.name, "menu1")
        self.assertEqual(menu.food_items, "test, test2, test3")
        self.assertEqual(menu.price, 10)
        self.assertEqual(menu.get_comma_seperated_food_items, "test, test2, test3")
        self.assertEqual(menu.get_price_in_dollars, "$10")

    def test_menu_model_should_have_fields(self):
        """menu model should have fields"""

        menu = MenuModel()
        self.assertTrue(hasattr(menu, "name"))
        self.assertTrue(hasattr(menu, "food_items"))
        self.assertTrue(hasattr(menu, "price"))
        self.assertTrue(hasattr(menu, "created_on"))
        self.assertTrue(hasattr(menu, "menu_image"))

    def test_menu_model_should_have_urls(self):
        """menu model should have absolute url"""

        menu = MenuModel()
        self.assertTrue(hasattr(menu, "get_absolute_url"))

    def test_menu_model_should_have_properties(self):
        """menu model should have created properties"""

        menu = MenuModel()
        self.assertTrue(hasattr(menu, "get_comma_seperated_food_items"))
        self.assertTrue(hasattr(menu, "get_price_in_dollars"))

    def test_menu_model_should_have_save_method(self):
        """menu model should have save save and delete method"""

        menu = MenuModel()
        self.assertTrue(hasattr(menu, "save"))
        self.assertTrue(hasattr(menu, "delete"))
        self.assertTrue(hasattr(menu, "get_absolute_url"))

    def test_menumodel_ordering(self):
        """menu model should have ordering"""

        menu1 = MenuModel.objects.get(name="menu1")
        menu2 = MenuModel.objects.get(name="menu2")
        menu3 = MenuModel.objects.get(name="menu3")
        self.assertEqual(list(MenuModel.objects.all()), [menu3, menu2, menu1])

    def test_food_items_is_comma_separated(self):
        """food items should be comma separated"""

        menu = MenuModel.objects.create(
            name="menu1", food_items="item1, item2, item3", price=1
        )
        self.assertEqual(menu.get_comma_seperated_food_items, "item1, item2, item3")


class MenuModelFormTest(TestCase):
    """Check if the food menu app form is valid or not"""

    def test_menu_model_form_should_have_required_fields(self):
        """menu model form should have required fields"""

        form = MenuForm()
        self.assertTrue(form.fields["name"].required)
        self.assertTrue(form.fields["food_items"].required)
        self.assertTrue(form.fields["price"].required)
        self.assertTrue(form.fields["menu_image"].required)

    def test_menu_model_form_should_have_validators(self):
        """menu model form should have [max_length, required, food_items_validator] validators"""

        form = MenuForm()
        self.assertEqual(len(form.fields["food_items"].validators), 3)

    def test_menu_model_form_should_have_clean_food_items_method(self):
        """menu model form should have save method"""

        form = MenuForm()
        self.assertTrue(hasattr(form, "clean_food_items"))


class FoodMenuViewTest(TestCase):
    """Check all the views of food menu app are working or not"""

    def test_food_menu_view_should_have_template(self):
        """food menu view should have template"""

        response = self.client.get("/food-menu/all/")
        self.assertTemplateUsed(response, "food_menus/menu_list.html")

    def test_food_menu_view_should_have_context(self):
        """food menu view should have context"""

        response = self.client.get("/food-menu/all/")
        self.assertEqual(type(response.context["menus"]), type(MenuModel.objects.all()))

    def test_radmin_foodmenu_view_required_login(self):
        """radmin food menu view should have template"""

        response = self.client.get("/food-menu/admin/")
        self.assertEqual(response.url, "/accounts/login/?next=/food-menu/admin/")

    def test_update_food_item_view(self):
        """update food item view should have template"""
        MenuModel.objects.create(
            name="menu1", food_items="item1, item2, item3", price=1
        )
        get_menu = MenuModel.objects.get(name="menu1")
        response = self.client.get(f"/food-menu/{get_menu.id}/update/")
        self.assertEqual(
            response.url, f"/accounts/login/?next=/food-menu/{get_menu.id}/update/"
        )


class FoodMenuRestaurantAdminViewTest(TestCase):
    """Check if the food menu restaurant admin view is working"""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="test", email="test@mail.com", password="test123"
        )
        self.client.force_login(self.user)

    def test_radmin_food_menu_view(self):
        """radmin food menu view should have template"""

        response = self.client.get("/food-menu/admin/")
        self.assertTemplateUsed(response, "food_menus/radmin_foodmenu.html")

    def test_food_menu_update_should_have_template(self):
        """food menu update should have template"""

        MenuModel.objects.create(
            name="menu1", food_items="item1, item2, item3", price=1
        )
        get_menu = MenuModel.objects.get(name="menu1")
        response = self.client.get(f"/food-menu/{get_menu.id}/update/")
        self.assertTemplateUsed(response, "food_menus/menu_update.html")

    def test_delete_food_menu_view(self):
        """delete food menu view should have template"""

        MenuModel.objects.create(
            name="menu1", food_items="item1, item2, item3", price=1
        )
        get_menu = MenuModel.objects.get(name="menu1")
        response = self.client.get(f"/food-menu/{get_menu.id}/delete/")
        self.assertEqual(response.status_code, 302)


class FoodMenuUrlsTest(TestCase):
    """Check all the urls for food menu app"""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="test", email="test@mail.com", password="test123"
        )
        self.client.force_login(self.user)

    def test_food_menus_urls_should_be_defined(self):
        """food menus urls should be defined"""

        MenuModel.objects.create(
            name="menu1", food_items="item1, item2, item3", price=1
        )
        get_menu = MenuModel.objects.get(name="menu1")

        self.assertEqual(reverse("menu_list"), "/food-menu/all/")
        self.assertEqual(reverse("menu_create"), "/food-menu/create/")
        self.assertEqual(
            reverse("menu_update", kwargs={"menu_id": get_menu.id}),
            f"/food-menu/{get_menu.id}/update/",
        )
        self.assertEqual(
            reverse("menu_delete", kwargs={"menu_id": get_menu.id}),
            f"/food-menu/{get_menu.id}/delete/",
        )

        self.assertEqual(reverse("admin_menu_list"), "/food-menu/admin/")
