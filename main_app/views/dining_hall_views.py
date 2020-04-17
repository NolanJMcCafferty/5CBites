from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from main_app.models import DiningHall, Rating


@login_required
def dining_hall_view(request):
    response = {}
    dining_hall_name = request.GET.get('name', '')

    if dining_hall_name:
        dining_hall = DiningHall.objects.filter(name=dining_hall_name).first()

        ratings = Rating.objects.filter(dining_hall=dining_hall)

        response = {
            'dining_hall': dining_hall,
            'ratings': ratings,
            'average_forks': ratings.aggregate(avg=Avg('forks'))['avg'],
        }

    return render(request, "dining_hall.html", response)
