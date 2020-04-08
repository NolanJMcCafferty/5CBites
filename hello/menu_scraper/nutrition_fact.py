from hello.models import NutritionFacts


class NutritionFact:
	
	def __init__(self, name, value, units):
		self.name = name
		self.value = value
		self.units = units

	def save(self):
		nutrition_fact, created = NutritionFacts.objects.get_or_create(name=self.name)

		if created:
			nutrition_fact.save()

		return nutrition_fact

	def get_value(self):
		return self.value

	def get_units(self):
		return self.units

	def __str__(self):
		return f"{self.name}: {self.value}{self.units}"
