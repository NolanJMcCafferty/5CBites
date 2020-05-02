from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from main_app.models import Rating
from main_app.views.views_constants import ratings_per_page, ratings_order_dict
from main_app.views.views_utils import save_dining_hall_rating, get_dining_hall


@login_required
def dining_hall_view(request, name):
    dining_hall = get_dining_hall(name)

    if request.method == 'POST':
        save_dining_hall_rating(request, dining_hall)

    rating_order = request.GET.get('ratings_order', 'recent')

    ratings = (
        Rating
        .objects
        .filter(dining_hall=dining_hall)
        .order_by(ratings_order_dict[rating_order])
    )

    ratings_paginator = Paginator(ratings, ratings_per_page)
    ratings_page_number = request.GET.get('page', 1)

    response = {
        'dining_hall': dining_hall,
        'rating_order': rating_order,
        'rating_orders': ratings_order_dict,
        'ratings_page': ratings_paginator.get_page(ratings_page_number),
        'average_forks': ratings.aggregate(avg=Avg('forks'))['avg'],
    }

    return render(request, "dining_hall.html", response)
