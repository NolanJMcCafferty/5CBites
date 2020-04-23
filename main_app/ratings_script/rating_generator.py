import os
import django
import random
from abc import ABC

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fivecbites.settings")
django.setup()
from main_app.models import Rating

MAX_RATING = 5.0


class RatingGenerator(ABC):

    def __init__(self, max_ratings_per_entry):
        self.entries = []
        self.positive_comments = []
        self.negative_comments = []
        self.num_forks = None
        self.rating_comment = None
        self.max_ratings_per_entry = max_ratings_per_entry

    @staticmethod
    def get_mean_ratings_for_entries(entries):
        new_entries = []

        for entry in entries:
            new_entries.append({
                'entry': entry,
                'mean_forks': random.randint(1, 4)
            })

        return new_entries

    def generate_ratings(self, user):
        ratings = []

        for entry in self.entries:
            num_ratings = random.randint(0, self.max_ratings_per_entry)
            for i in range(num_ratings):
                ratings.append(self.generate_rating(user, entry))

        Rating.objects.bulk_create(ratings)

    def generate_rating(self, user, entry):
        self.num_forks = entry['mean_forks'] + random.gauss(0.0, 1.0)

        # clip the edges
        if self.num_forks > 5.0:
            self.num_forks = 5.0
        if self.num_forks < 0.0:
            self.num_forks = 0.0

        rating_comments = self.positive_comments if self.num_forks > (MAX_RATING / 2.0) else self.negative_comments
        self.rating_comment = random.choice(rating_comments) if abs(self.num_forks - MAX_RATING / 2.0) > 1.5 else ""
