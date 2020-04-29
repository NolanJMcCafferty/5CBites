from main_app.models import DiningHall, DietaryRestrictions, User


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
