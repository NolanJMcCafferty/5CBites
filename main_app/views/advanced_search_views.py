import pandas as pd
from django.shortcuts import render
from main_app.models import Dish, Rating
from django.db.models import Avg
from main_app.views.views_utils import get_dining_halls, get_diets, get_allergens
from main_app.views.views_constants import num_results


def advanced_search_view(request):
    response = {
        'dining_halls': get_dining_halls(),
        'diets': get_diets(),
        'allergens': get_allergens(),
        'results': get_most_popular_results(request),
    }

    return render(request, 'advanced_search.html', response)


def get_search_results(request):
    results = Dish.objects.all()

    if request.method == "POST":
        if request.POST['dining_hall'] != 'any':
            results = results.filter(dining_hall=request.POST['dining_hall'])

        if request.POST['dish_name']:
            results = results.filter(name=request.POST['dish_name'])

        if request.POST['diet'] != 'any':
            results = results.filter(dietaryrestrictionsofdish__dietary_restriction__name=request.POST['diet'])

        if request.POST.getlist('allergens') != ['any']:

            results = results.exclude(
                dietaryrestrictionsofdish__dietary_restriction__name__in=request.POST.getlist('allergens')
            )

    return pd.DataFrame(results.values())


def get_most_popular_results(request):
    result_rows = get_search_results(request)
    avg_dish_ratings = get_avg_dish_ratings(request)

    if result_rows.empty or avg_dish_ratings.empty:
        results = []
    else:
        results = pd.merge(
            result_rows,
            avg_dish_ratings,
            left_on='id',
            right_on='dish_id',
        ).sort_values(
            'avg_rating',
            ascending=False
        ).head(num_results).to_dict('records')

    return results


def get_avg_dish_ratings(request):
    avg_ratings = Rating.objects.filter(dish__isnull=False)

    if request.method == "POST":

        if request.POST['role'] != 'any':
            avg_ratings = avg_ratings.filter(user__role=request.POST['role'])

        if request.POST['school'] != 'any':
            avg_ratings = avg_ratings.filter(user__school=request.POST['school'])

        if request.POST['grad_year'] != 'any':
            avg_ratings = avg_ratings.filter(user__grad_year=request.POST['grad_year'])

    return pd.DataFrame(
        avg_ratings.values('dish_id')
        .annotate(avg_rating=Avg('forks'))
        .order_by('-avg_rating')
    )
