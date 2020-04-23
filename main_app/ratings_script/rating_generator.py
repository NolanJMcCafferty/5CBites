import os
import django
import random
from abc import ABC

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fivecbites.settings")
django.setup()
from main_app.models import User, Rating

MAX_RATING = 5.0


class RatingGenerator(ABC):

    def __init__(self):
        self.entries = []
        self.positive_comments = []
        self.negative_comments = []
        self.num_forks = None
        self.rating_comment = None
        self.user = User.objects.order_by("?").first()

    def generate_ratings(self, max_ratings_per_entry):
        ratings = []

        for entry in self.entries:
            num_ratings = random.randint(0, max_ratings_per_entry)
            for i in range(num_ratings):
                ratings.append(self.generate_rating(entry))

        Rating.objects.bulk_create(ratings)

    def generate_rating(self, entry):
        self.num_forks = random.random() * MAX_RATING
        rating_comments = self.positive_comments if self.num_forks > (MAX_RATING / 2.0) else self.negative_comments
        self.rating_comment = random.choice(rating_comments) if abs(self.num_forks - MAX_RATING / 2.0) > 1.5 else ""
