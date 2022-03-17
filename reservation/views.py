import datetime

from django.utils.dateparse import parse_time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist

from food_menus.models import MenuModel
from users.models import RestaurantAdmin
from users.forms import (
    RestaurantAdminForm,
    RestaurantAdminAdd,
    RestaurantAdminLoginForm,
    UserUpdateForm,
)
from .models import RestaurantModel, TableModel, ReservationModel
from .forms import CreateRestaurantForm, CreateTableForm


# ===================================
# User Restriction Check
# ===================================
def is_radmin_check(user):
    """Restricts access to only super user and active restaurant admin.
    - Super user can access all views
    - Active restaurant admin can access all restaurand-admin views
    - Nomal user and inactive restaurant admin can not access all(restaurand-admin) views
    - Parameter for @user_passes_test decorator

    Returns:
        _type_: Boolean
    """

    if user.is_superuser:
        return True
    else:
        try:
            if user.restaurant_admin.is_active:
                return True
            else:
                return False
        except ObjectDoesNotExist:
            return False


def superuser_only_check(user):
    """Restricts access to only super user.
    - Super user can access all views
    - Parameter for @user_passes_test decorator

    Returns:
        _type_: Boolean
    """

    if user.is_superuser:
        return True
    else:
        return False


# ================================================
# Home Page View, Restaurant Admin Login View
# ================================================
def index_view(request):
    food_menus = MenuModel.objects.all()[:10]
    return render(request, "pages/index.html", {"food_menus": food_menus})


def admin_login_view(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                if user.restaurant_admin.is_active:
                    login(request, user)
                    messages.success(
                        request, f"Logged in successfully as {user.username}"
                    )
                    return redirect("admin_dashboard")
                messages.error(request, f"{user.username} is not an active admin!")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            except ObjectDoesNotExist:
                if user.is_superuser:
                    login(request, user)
                    messages.success(
                        request, f"Logged in successfully as {user.username}"
                    )
                    return redirect("admin_dashboard")
                else:
                    messages.error(
                        request, f"{user.username} is not a restaurant admin"
                    )
                    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "Invalid credentials")
            return redirect("admin_login")
    else:
        form = RestaurantAdminLoginForm()

    return render(request, "restaurant_admin/login_admin.html", {"form": form})


@login_required
@user_passes_test(is_radmin_check)
def admin_logout_view(request):
    logout(request)
    return redirect("/")


# ================================================
# Admin manage restaurant, tables and reservations
# ================================================
@login_required
@user_passes_test(superuser_only_check)
def add_admin_view(request):
    if request.method == "POST":
        user_form = RestaurantAdminAdd(request.POST)
        admin_form = RestaurantAdminForm(
            request.POST,
            request.FILES,
        )
        if user_form.is_valid():
            if admin_form.is_valid():
                user = user_form.save()
                restaurant_admin = admin_form.save(commit=False)
                restaurant_admin.user = user
                restaurant_admin.save()
                messages.success(request, "Restaurant-Admin added successfully!")
                messages.info(
                    request,
                    f"Restaurant-Admin login details: Username: {user.username} | Password: YOUR-PASSWORD",
                )

                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            messages.error(request, f"Errors: </hr> {admin_form.errors}")
        else:
            messages.error(request, f"Errors: </hr> {user_form.errors}")
            if admin_form.errors:
                messages.error(request, f"Errors: </hr> {admin_form.errors}")

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
@user_passes_test(superuser_only_check)
def update_admin_view(request, username):
    user = User.objects.get(username=username)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        admin_form = RestaurantAdminForm(
            request.POST,
            request.FILES,
            instance=user.restaurant_admin,
        )
        if user_form.is_valid():
            if admin_form.is_valid():
                user_form.save()
                admin_form.save()
                messages.success(request, "Restaurant-Admin updated successfully!")

                return redirect("all_admins")
    else:
        user_form = UserUpdateForm(instance=request.user)
        admin_form = RestaurantAdminForm(instance=user.restaurant_admin)

    return render(
        request,
        "restaurant_admin/update_admin.html",
        {"form": (user_form, admin_form)},
    )


@login_required
@user_passes_test(superuser_only_check)
def delete_admin_view(request, username):
    user = User.objects.get(username=username)
    user.delete()
    messages.success(request, "Restaurant-Admin deleted successfully!")
    return redirect("all_admins")


@login_required
@user_passes_test(superuser_only_check)
def all_restaurant_admin_view(request):
    restaurant_admins = RestaurantAdmin.objects.all()
    user_form = RestaurantAdminAdd()
    admin_form = RestaurantAdminForm()
    return render(
        request,
        "restaurant_admin/admins.html",
        {"restaurant_admins": restaurant_admins, "form": (user_form, admin_form)},
    )


@login_required
@user_passes_test(is_radmin_check)
def restaurant_admin_dashboard(request):
    restaurant = RestaurantModel.objects.all()[0]
    tables = TableModel.objects.all()
    tables_with_next_reservation = []
    for table in tables:
        if table.reservations:
            next_reservation = table.reservations.filter(
                reservation_date__gte=timezone.now().date(),
            ).order_by("reservation_date", "reservation_time")
            if next_reservation:
                tables_with_next_reservation.append((table, next_reservation[0]))
            else:
                tables_with_next_reservation.append((table, None))

        else:
            tables_with_next_reservation.append((table, None))
    form = CreateTableForm()

    context = {
        "restaurant": restaurant,
        "tables": tables,
        "tables_n_reservation": tables_with_next_reservation,
        "form": form,
    }

    return render(request, "restaurant_admin/dashboard.html", context=context)


@login_required
@user_passes_test(is_radmin_check)
def todays_reservations_admin_view(request):
    reservations = ReservationModel.objects.filter(
        reservation_date=timezone.now().date()
    )

    context = {
        "reservations": reservations,
    }

    return render(request, "restaurant_admin/todays.html", context=context)


@login_required
@user_passes_test(is_radmin_check)
def upcoming_reservations_admin_view(request):
    upcoming_reservations = ReservationModel.objects.filter(
        reservation_date__gte=timezone.now().date()
    )

    context = {
        "reservations": upcoming_reservations,
    }

    return render(
        request, "restaurant_admin/upcoming_reservations.html", context=context
    )


@login_required
@user_passes_test(is_radmin_check)
def past_reservations_admin_view(request):
    past_reservations = ReservationModel.objects.filter(
        reservation_date__lt=timezone.now().date()
    )

    context = {
        "reservations": past_reservations,
    }

    return render(request, "restaurant_admin/past_reservations.html", context=context)


@login_required
@user_passes_test(is_radmin_check)
def create_restaurant_view(request):
    my_restaurant = RestaurantModel.objects.all()[0]
    if my_restaurant:
        messages.warning(
            request, "You already created a restaurant, you can update it."
        )
        return redirect("admin_dashboard")
    if request.method == "POST":
        form = CreateRestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.save()
            messages.success(request, "Your Restaurant is created successfully")
            return redirect("admin_dashboard")
    else:
        form = CreateRestaurantForm()

    return render(request, "restaurant_admin/create_restaurant.html", {"form": form})


@login_required
@user_passes_test(is_radmin_check)
def update_resturant_view(request):
    my_restaurant = RestaurantModel.objects.all()[0]
    if my_restaurant:
        if request.method == "POST":
            form = CreateRestaurantForm(request.POST, instance=my_restaurant)
            if form.is_valid():
                restaurant = form.save(commit=False)
                restaurant.save()
                messages.success(
                    request, "Restaurant's informations are updated successfully"
                )
                return redirect("admin_dashboard")
        else:
            form = CreateRestaurantForm(instance=my_restaurant)
    else:
        messages.warning(request, "You don't have a restaurant yet. Add one first.")
        return redirect("admin_dashboard")
    return render(request, "restaurant_admin/update_restaurant.html", {"form": form})


@login_required
@user_passes_test(is_radmin_check)
def add_table_view(request):
    my_restaurant = RestaurantModel.objects.all()[0]
    if my_restaurant:
        if request.method == "POST":
            form = CreateTableForm(request.POST)
            if form.is_valid():
                table = form.save(commit=False)
                table.restaurant = my_restaurant
                table_number = table.table_number
                table.save()
                messages.success(
                    request, f"Table #{table_number} is created successfully"
                )
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        else:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        messages.warning(request, "You don't have a restaurant yet. Add one first.")


@login_required
@user_passes_test(is_radmin_check)
def update_table_view(request, table_id):
    table = get_object_or_404(TableModel, id=table_id)
    if request.method == "POST":
        form = CreateTableForm(request.POST, instance=table)
        if form.is_valid():
            table = form.save(commit=False)
            table.save()
            messages.success(
                request,
                f"Table #{table.table_number} informations are updated successfully",
            )
            return redirect("admin_dashboard")
    else:
        form = CreateTableForm(instance=table)
    return render(
        request, "restaurant_admin/update_table.html", {"form": form, "table": table}
    )


@login_required
@user_passes_test(is_radmin_check)
def delete_table_view(request, table_id):
    table = get_object_or_404(TableModel, id=table_id)
    table.delete()
    messages.success(request, f"Table #{table.table_number} is deleted successfully")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


# =======================================
# Customer manage reservation
# =======================================
@login_required
def make_reservation_view(request):
    restaurant = RestaurantModel.objects.all()[0]
    tables = TableModel.objects.all()
    times = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
    if request.method == "POST":
        date = request.POST["date"]
        time = request.POST["time"]
        table_code = request.POST["table_size"]
        message = request.POST["message"]

        customer = request.user
        table = TableModel.objects.filter(table_number=table_code).first()
        parsed_date = datetime.datetime.strptime(date, "%m/%d/%Y").date()
        parsed_time = parse_time(time)

        if parsed_date >= timezone.now().date():
            if ReservationModel.objects.filter(
                customer=customer,
                table=table,
                reservation_date=parsed_date,
                reservation_time=parsed_time,
            ).exists():
                messages.error(
                    request, "This table is already reserved for the date or time."
                )
                return redirect("make_reservation")
            else:
                reservation = ReservationModel.objects.create(
                    customer=customer,
                    table=table,
                    reservation_date=parsed_date,
                    reservation_time=parsed_time,
                    message=message,
                )
                reservation.save()
                return render(
                    request,
                    "reservation/confirm.html",
                    {"date": date, "time": time, "table": table_code},
                )
        else:
            messages.error(request, "You can't reserve a table in the past!")
            return redirect("make_reservation")

    else:
        context = {
            "restaurant": restaurant,
            "tables": tables,
            "available_times": times,
        }
        return render(request, "reservation/make_reservation.html", context=context)


@login_required
def cancel_reservation_view(request, reservation_id):
    reservation = get_object_or_404(ReservationModel, id=reservation_id)
    table_no = reservation.table.table_number
    datetime = (
        f'at {reservation.reservation_time.strftime("%I:%M %p")} '
        + f'on {reservation.reservation_date.strftime("%m/%d/%Y")}'
    )

    reservation.delete()
    messages.success(
        request,
        f"Your reservation for Table #{table_no} {datetime} is canceled successfully",
    )

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def user_reservations_view(request):
    reservations = ReservationModel.objects.filter(customer=request.user)
    return render(
        request, "reservation/user_reservations.html", {"reservations": reservations}
    )
