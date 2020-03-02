
class FoodItem():

	def __init__(self, name, tier=None):
		self.name = name
		self.tier = tier

	def __str__(self):
		return f"name: {self.name}, tier: {self.tier}"