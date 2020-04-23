import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fivecbites.settings")
django.setup()

from main_app.models import User
from dish_rating_generator import DishRatingGenerator
from dining_hall_rating_generator import DiningHallRatingGenerator

if __name__ == "__main__":
    users = User.objects.all()

    dish_rating_generator = DishRatingGenerator(2)
    dining_hall_rating_generator = DiningHallRatingGenerator(5)

    for user in users:
        dish_rating_generator.generate_ratings(user)
        dining_hall_rating_generator.generate_ratings(user)
