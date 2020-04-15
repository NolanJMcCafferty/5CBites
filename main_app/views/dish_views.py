from django.shortcuts import render
from django.db.models import Avg
from main_app.models import Dish, Rating, NutritionFactsOfDish, DietaryRestrictionsOfDish, \
    IngredientsInDish


def dish_view(request):
    response = {}
    dish_id = request.GET.get('id', '')

    if dish_id:
        dish = Dish.objects.filter(id=dish_id).first()

        ratings = Rating.objects.filter(dish=dish)

        response = {
            'dish': dish,
            'ratings': ratings,
            'average_forks': ratings.aggregate(avg=Avg('forks'))['avg'],
            'nutrition_facts': NutritionFactsOfDish.objects.filter(dish=dish),
            'dietary_restrictions': DietaryRestrictionsOfDish.objects.filter(dish=dish),
            'ingredients': IngredientsInDish.objects.filter(dish=dish),
        }

    return render(request, 'dish.html', response)
