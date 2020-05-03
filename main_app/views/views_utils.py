import datetime
from main_app.models import DiningHall, DietaryRestrictions, User, Rating, Dish, NutritionFactsOfDish, \
    DietaryRestrictionsOfDish, IngredientsInDish, NutritionFacts
from main_app.views.views_constants import primary_nutrition_facts, nutrition_fact_names, dates_list


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


def get_all_nutrition_facts():
    return (
        NutritionFacts
        .objects
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
    primary_facts = []
    secondary_facts = []
    calories = None
    serving_size = None

    all_facts = (
        NutritionFactsOfDish
        .objects
        .filter(dish=dish)
    )

    for fact in all_facts:

        if fact.nutrition_fact.name in nutrition_fact_names:
            fact_name = nutrition_fact_names[fact.nutrition_fact.name]
        else:
            fact_name = fact.nutrition_fact.name

        new_fact = {
            'name': fact_name,
            'value': str(fact.value) + fact.units,
        }

        if fact_name == 'calories':
            calories = new_fact['value']
        elif fact_name == 'serving size':
            serving_size = new_fact['value']
        elif fact_name in primary_nutrition_facts:
            primary_facts.append(new_fact)
        else:
            secondary_facts.append(new_fact)

    return {
        'calories': calories,
        'serving_size': serving_size,
        'facts': zip(primary_facts, secondary_facts)
    }


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


def get_dates():
    return dates_list
