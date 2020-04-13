from rating_generator import RatingGenerator
from main_app.models import DiningHall, Rating
from comment_constants import dining_hall_positive_comments, dining_hall_negative_comments
from django.utils import timezone


class DiningHallRatingGenerator(RatingGenerator):

    def __init__(self):
        super().__init__()
        self.entries = DiningHall.objects.all()
        self.positive_comments = dining_hall_positive_comments
        self.negative_comments = dining_hall_negative_comments

    def generate_rating(self, entry):
        super().generate_rating(entry)

        return Rating(
            user=self.user,
            datetime=timezone.now(),
            forks=self.num_forks,
            comment=self.rating_comment,
            dish=None,
            dining_hall=entry,
        )
