import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F
from main_app.forms import CustomUserCreationForm
from main_app.models import Meal, MenuItem, Rating
from main_app.views.views_utils import save_dining_hall_rating, save_dish_rating, get_dish, get_dining_hall

today = datetime.datetime.today()


def sign_up_view(request):
    errors = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            errors = form.errors
    else:
        form = CustomUserCreationForm()
    return render(request, 'login.html', {'form': form, 'sign_up': True, 'errors': errors})


def login_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect to home page
            return redirect('home')
        else:
            return render(request, "login.html", {'message': 'Invalid Login'})
    else:
        return render(request, "login.html", {'message': ''})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')


@login_required
def home_view(request):
    if request.method == "POST":
        if request.POST.get('dish'):
            save_dish_rating(request, get_dish(request.POST.get('dish')))
        else:
            save_dining_hall_rating(request, get_dining_hall(request.POST.get('dining_hall')))

    response = {
        'favorites': get_favorite_daily_dishes(request)
    }

    return render(request, 'home.html', response)


def get_favorite_daily_dishes(request):

    todays_favorites = (
        Rating
        .objects
        .filter(
            user=request.user,
            dish__menuitem__meal__start_time__date=today,
        )
        .annotate(
            meal_available=F('dish__menuitem__meal__name'),
        )
        .distinct()
        .order_by('-forks')[:10]
    )

    return todays_favorites


@login_required
def menus_view(request):
    meal_types = []

    if request.method == "POST":
        if request.POST.get('dish'):
            save_dish_rating(request, get_dish(request.POST.get('dish')))
        else:
            save_dining_hall_rating(request, get_dining_hall(request.POST.get('dining_hall')))

    for meal_type in get_meal_types_today():
        meals = []
        meals_offered = Meal.objects.filter(
            start_time__date=today,
            name=meal_type,
        )

        for meal in meals_offered:
            stations = []
            station_names = get_meal_stations(meal)

            for station in station_names:
                stations.append({
                    'name': station,
                    'menu_items': get_menu_items_in_station(meal, station)
                })

            meals.append({
                'info': meal,
                'stations': stations,
            })

        meal_types.append({
            'name': meal_type,
            'meals': meals,
        })

    return render(request, 'menus.html', {'meal_types': meal_types})


def get_meal_types_today():

    return (
        Meal
        .objects
        .filter(start_time__date=today)
        .values_list('name', flat=True)
        .distinct()
    )


def get_meal_stations(meal):
    return (
        MenuItem
        .objects
        .filter(meal=meal)
        .exclude(station='-')
        .values_list('station', flat=True)
        .distinct()
    )


def get_menu_items_in_station(meal, station):
    return (
        MenuItem
        .objects
        .filter(
            meal=meal,
            station=station
        )
    )

