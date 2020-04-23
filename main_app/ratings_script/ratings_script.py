from dish_rating_generator import DishRatingGenerator
from dining_hall_rating_generator import DiningHallRatingGenerator


if __name__ == "__main__":
    for i in range(30):
        print("Generating ratings for user number" + str(i))
        dish_rating_generator = DishRatingGenerator()
        dining_hall_rating_generator = DiningHallRatingGenerator()
        dish_rating_generator.generate_ratings(5)
        dining_hall_rating_generator.generate_ratings(10)
