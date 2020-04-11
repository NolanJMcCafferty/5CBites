import re
from nutrition_fact import NutritionFact
from nutrition_fact_constants import sodexo_nutrition_facts
from hello.models import Dish, NutritionFactsOfDish


class FoodItem:

	def __init__(self, name, dining_hall, nutrition_facts):
		self.name = name
		self.nutrition_facts = []
		self.dish = None

		if nutrition_facts:
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
			nutrition_fact = NutritionFact(
				name=fact_dict['label'], 
				value=fact_dict['value'].replace('lessthan', ''),
				units=fact_dict['unit'],
			)
			self.nutrition_facts.append(nutrition_fact)

	def parse_sodexo_nutrition_facts(self, nutrition_facts):
		for fact_name, value in nutrition_facts.items():
			if fact_name in sodexo_nutrition_facts:
				value = value.replace('<', '')

				nutrition_fact = NutritionFact(
					name=fact_name, 
					value=re.sub('[a-zA-Z]', '', value),
					units="".join(re.findall('[a-zA-Z]', value))
				)
				self.nutrition_facts.append(nutrition_fact)

	def parse_po_nutrition_facts(self, nutrition_facts):
		self.add_po_serving_size(nutrition_facts)

		for fact_text in nutrition_facts[1:]:
			fact_list = re.split('\(|\):', fact_text)
			
			nutrition_fact = NutritionFact(
				name=fact_list[0].strip(),
				value=fact_list[2].strip(),
				units=fact_list[1],
			)
			self.nutrition_facts.append(nutrition_fact)
	
	def add_po_serving_size(self, nutrition_facts):
		serving_size = re.split(':', nutrition_facts[0])
		value_list = serving_size[1].strip().split()
		value = value_list[0]
		units = " ".join(value_list[1:])
		
		nutrition_fact = NutritionFact(
			name=serving_size[0].strip(),
			value=value,
			units=units,
		)

		self.nutrition_facts.append(nutrition_fact)

	def save(self, dining_hall):
		self.dish, _ = Dish.objects.get_or_create(name=self.name, dining_hall=dining_hall)

		nutrition_fact_records = self.save_nutrition_facts()

		return self.dish, nutrition_fact_records

	def save_nutrition_facts(self):
		nutrition_fact_records = []
		for nutrition_fact in self.nutrition_facts:
			fact = nutrition_fact.save()

			NutritionFactsOfDish.objects.filter(
				dish=self.dish,
				nutrition_fact=fact,
			).delete()

			record = NutritionFactsOfDish(
				dish=self.dish,
				nutrition_fact=fact,
				value=nutrition_fact.get_value(),
				units=nutrition_fact.get_units(),
			)
			nutrition_fact_records.append(record)

		return nutrition_fact_records

	def __str__(self):
		return (
			f"\t - {self.name}\n\t\t* " + 
			"\n\t\t* ".join([str(fact) for fact in self.nutrition_facts])
		)