import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from main_app.models import Meal, MenuItem


def sign_up_view(request):
    return render(request, "login.html", {'message': ''})


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
        return redirect('login_view')


def home_view(request):
    return render(request, 'base.html', {})


def menus_view(request):
    meal_types = []
    today = datetime.datetime.today()

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
    today = datetime.datetime.today()

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
