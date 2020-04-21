from main_app.models import DiningHall, DietaryRestrictions


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
