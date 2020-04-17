import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from main_app.models import Dish, Rating, NutritionFactsOfDish, DietaryRestrictionsOfDish, \
    IngredientsInDish


@login_required
def dish_view(request, dish_id):
    dish = Dish.objects.filter(id=dish_id).first()

    if request.method == 'POST':
        save_dish_rating(request, dish)

    ratings = Rating.objects.filter(dish=dish).order_by('-datetime')

    response = {
        'dish': dish,
        'ratings': ratings,
        'average_forks': ratings.aggregate(avg=Avg('forks'))['avg'],
        'nutrition_facts': NutritionFactsOfDish.objects.filter(dish=dish),
        'dietary_restrictions': DietaryRestrictionsOfDish.objects.filter(dish=dish),
        'ingredients': IngredientsInDish.objects.filter(dish=dish),
    }

    return render(request, 'dish.html', response)


def save_dish_rating(request, dish):
    Rating.objects.create(
        user=request.user,
        forks=request.POST['forks'],
        comment=request.POST['comment'],
        datetime=datetime.datetime.now(),
        dish=dish,
        dining_hall=None,
    )
