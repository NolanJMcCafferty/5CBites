from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from main_app.models import Rating
from main_app.views.views_constants import ratings_per_page, ratings_order_dict
from main_app.views.views_utils import save_dish_rating, get_dish, get_nutrition_facts, get_dietary_restrictions, \
    get_ingredients


@login_required
def dish_view(request, dish_id):
    dish = get_dish(dish_id)

    if request.method == 'POST':
        save_dish_rating(request, dish)

    rating_order = request.GET.get('ratings_order', 'recent')

    ratings = (
        Rating
        .objects
        .filter(dish=dish)
        .order_by(ratings_order_dict[rating_order])
    )

    ratings_paginator = Paginator(ratings, ratings_per_page)
    ratings_page_number = request.GET.get('page', 1)

    response = {
        'dish': dish,
        'rating_order': rating_order,
        'rating_orders': ratings_order_dict,
        'ratings_page': ratings_paginator.get_page(ratings_page_number),
        'average_forks': ratings.aggregate(avg=Avg('forks'))['avg'],
        'nutrition_facts': get_nutrition_facts(dish),
        'dietary_restrictions': get_dietary_restrictions(dish),
        'ingredients': get_ingredients(dish),
    }

    return render(request, 'dish.html', response)
