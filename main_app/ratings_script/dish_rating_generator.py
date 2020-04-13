from rating_generator import RatingGenerator
from main_app.models import Dish, Rating
from comment_constants import dish_positive_comments, dish_negative_comments
from django.utils import timezone


class DishRatingGenerator(RatingGenerator):

    def __init__(self):
        super().__init__()
        self.entries = Dish.objects.all()
        self.positive_comments = dish_positive_comments
        self.negative_comments = dish_negative_comments

    def generate_rating(self, entry):
        super().generate_rating(entry)

        return Rating(
            user=self.user,
            datetime=timezone.now(),
            forks=self.num_forks,
            comment=self.rating_comment,
            dish=entry,
            dining_hall=None,
        )
