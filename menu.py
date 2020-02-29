
class Menu():

	def __init__(self, dining_hall, date):
		self.dining_hall = dining_hall
		self.date = date
		self.meals = []

	def add_meal(self, meal):
		self.meals.append(meal)


	def __str__(self):
		return (
			f"{self.dining_hall}: {self.date}\n     ----------------------------------" +
			"\n".join([str(meal) for meal in self.meals])
		)




