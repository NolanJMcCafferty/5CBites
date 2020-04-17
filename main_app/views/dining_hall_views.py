import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from main_app.models import DiningHall, Rating


@login_required
def dining_hall_view(request, name):
    dining_hall = DiningHall.objects.filter(name=name).first()

    if request.method == 'POST':
        save_dining_hall_rating(request, dining_hall)

    ratings = Rating.objects.filter(dining_hall=dining_hall).order_by('-datetime')

    response = {
        'dining_hall': dining_hall,
        'ratings': ratings,
        'average_forks': ratings.aggregate(avg=Avg('forks'))['avg'],
    }

    return render(request, "dining_hall.html", response)


def save_dining_hall_rating(request, dining_hall):
    Rating.objects.create(
        user=request.user,
        forks=request.POST['forks'],
        comment=request.POST['comment'],
        datetime=datetime.datetime.now(),
        dish=None,
        dining_hall=dining_hall,
    )