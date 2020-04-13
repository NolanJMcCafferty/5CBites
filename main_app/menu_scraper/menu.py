from main_app.models import Meal, DiningHall, NutritionFactsOfDish


class Menu:

	def __init__(self, dining_hall, meal_name, start_time, end_time, day_of_week):
		self.dining_hall = dining_hall
		self.meal_name = meal_name
		self.start_time = start_time
		self.end_time = end_time
		self.day_of_week = day_of_week
		self.stations = []
		self.meal = None

	def add_station(self, station):
		self.stations.append(station)

	def get_stations(self):
		return self.stations

	def save(self):
		dining_hall = DiningHall.objects.filter(name=self.dining_hall).first()
		self.meal, _ = Meal.objects.get_or_create(
			name=self.meal_name,
			dining_hall=dining_hall,
			day_of_week=self.day_of_week,
			start_time=self.start_time,
			end_time=self.end_time,
		)

		self.save_stations()

	def save_stations(self):
		nutrition_fact_records = []
		for station in self.stations:
			nf_records = station.save(self.meal)
			nutrition_fact_records += nf_records

		NutritionFactsOfDish.objects.bulk_create(nutrition_fact_records)

	def __str__(self):
		return (
			f"\n\n{self.dining_hall} | {self.meal_name} | {self.start_time}-{self.end_time} \n" +
			"\n".join([str(station) for station in self.stations])
		)




