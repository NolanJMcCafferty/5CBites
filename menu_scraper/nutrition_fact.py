
class NutritionFact():
	
	def __init__(self, name, value, units):
		self.name = name
		self.value = value
		self.units = units

	def __str__(self):
		return f"{self.name}: {self.value}{self.units}"
