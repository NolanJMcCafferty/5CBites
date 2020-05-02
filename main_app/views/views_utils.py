import datetime
from main_app.models import DiningHall, DietaryRestrictions, User, Rating, Dish, NutritionFactsOfDish, \
    DietaryRestrictionsOfDish, IngredientsInDish


def get_dining_halls():
    return (
        DiningHall
        .objects
        .all()
        .distinct()
    )


def get_diets():
    return (
        DietaryRestrictions
        .objects
        .filter(name__startswith='is')
        .distinct()
    )


def get_allergens():
    return (
        DietaryRestrictions
        .objects
        .exclude(name__startswith='is')
        .distinct()
    )


def get_roles():
    return (
        User
        .objects
        .values_list('role', flat=True)
        .distinct()
    )


def get_schools():
    return (
        User
        .objects
        .values_list('school', flat=True)
        .distinct()
    )


def get_grad_years():
    grad_years = (
        User
        .objects
        .values_list('grad_year', flat=True)
        .order_by('grad_year')
        .distinct()
    )

    return [grad_year if grad_year else 'NA' for grad_year in grad_years]


def get_dish(dish_id):
    return (
        Dish
        .objects
        .filter(id=dish_id)
        .first()
    )


def get_dining_hall(name):
    return (
        DiningHall
        .objects
        .filter(name=name)
        .first()
    )


def save_dish_rating(request, dish):
    Rating.objects.create(
        user=request.user,
        forks=request.POST['forks'],
        comment=request.POST['comment'],
        datetime=datetime.datetime.now(),
        dish=dish,
        dining_hall=None,
    )


def save_dining_hall_rating(request, dining_hall):
    Rating.objects.create(
        user=request.user,
        forks=request.POST['forks'],
        comment=request.POST['comment'],
        datetime=datetime.datetime.now(),
        dish=None,
        dining_hall=dining_hall,
    )


def get_nutrition_facts(dish):
    return (
        NutritionFactsOfDish
        .objects
        .filter(dish=dish)
    )


def get_dietary_restrictions(dish):
    return (
        DietaryRestrictionsOfDish
        .objects
        .filter(dish=dish)
    )


def get_ingredients(dish):
    return (
        IngredientsInDish
        .objects
        .filter(dish=dish)
    )
