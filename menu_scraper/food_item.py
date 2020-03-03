from nutrition_fact import NutritionFact
from nutrition_fact_constants import sodexo_nutrition_facts

class FoodItem():

	def __init__(self, name, dining_hall, nutrition_facts):
		self.name = name
		self.nutrition_facts = []

		self.parse_nutrition_facts(dining_hall, nutrition_facts)

	def parse_nutrition_facts(self, dining_hall, nutrition_facts):

		if dining_hall == 'bon appetite':
			self.parse_ba_nutrition_facts(nutrition_facts)
		elif dining_hall == 'sodexo':
			self.parse_sodexo_nutrition_facts(nutrition_facts)
		else:
			self.parse_po_nutrition_facts(nutrition_facts)

	def parse_ba_nutrition_facts(self, nutrition_facts):
		for key, fact_dict in nutrition_facts.items():
			value = fact_dict['value'] + fact_dict['unit']
			nutrition_fact = NutritionFact(
				fact_dict['label'], 
				value.replace('lessthan', ''),
				)
			self.nutrition_facts.append(nutrition_fact)

	def parse_sodexo_nutrition_facts(self, nutrition_facts):
		for fact_name, value in nutrition_facts.items():
			if fact_name in sodexo_nutrition_facts:

				nutrition_fact = NutritionFact(
					fact_name, 
					value.replace('<', ''),
				)
				self.nutrition_facts.append(nutrition_fact)


	def __str__(self):
		return (
			f"\t - {self.name}\n\t\t* " + 
			"\n\t\t* ".join([str(fact) for fact in self.nutrition_facts])
		)