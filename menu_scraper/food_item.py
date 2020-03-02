
class FoodItem():

	def __init__(self, name):
		self.name = name

	def __str__(self):
		return f"\t - {self.name}"