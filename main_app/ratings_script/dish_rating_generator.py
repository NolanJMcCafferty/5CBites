from rating_generator import RatingGenerator
from main_app.models import Dish, Rating
from comment_constants import dish_positive_comments, dish_negative_comments
from django.utils import timezone


class DishRatingGenerator(RatingGenerator):

    def __init__(self, max_ratings_per_entry):
        super().__init__(max_ratings_per_entry)
        self.entries = RatingGenerator.get_mean_ratings_for_entries(Dish.objects.all())
        self.positive_comments = dish_positive_comments
        self.negative_comments = dish_negative_comments

    def generate_rating(self, user, entry):
        super().generate_rating(user, entry)

        return Rating(
            user=user,
            datetime=timezone.now(),
            forks=self.num_forks,
            comment=self.rating_comment,
            dish=entry['entry'],
            dining_hall=None,
        )
