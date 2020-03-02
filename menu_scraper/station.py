
class Station():

	def __init__(self, name):
		self.name = name
		self.food_items = []

	def add_food_item(self, food_item):
		self.food_items.append(food_item)

	def __str__(self):
		return (
			f"\n{self.name}\n" +
			"\n".join([str(food_item) for food_item in self.food_items])
		)