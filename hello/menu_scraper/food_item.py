import re
from nutrition_fact import NutritionFact
from food_item_constants import sodexo_nutrition_facts, sodexo_dietary_restrictions
from hello.models import Dish, NutritionFactsOfDish, DietaryRestrictions, DietaryRestrictionsOfDish


class FoodItem:

	def __init__(self, name, dining_hall, nutrition_facts, ingredients):
		self.name = name
		self.nutrition_facts = []
		self.dietary_restrictions = []
		self.ingredients = set()
		self.dish = None

		self.parse_food_details(dining_hall, nutrition_facts, ingredients)

	def parse_food_details(self, dining_hall, nutrition_facts, ingredients):

		if dining_hall == 'bon appetite':
			self.parse_ba_nutrition_facts(nutrition_facts)
		elif dining_hall == 'sodexo':
			self.parse_sodexo_nutrition_facts(nutrition_facts)
			self.parse_sodexo_dietary_restrictions(nutrition_facts)
		else:
			self.parse_po_nutrition_facts(nutrition_facts)
			self.parse_po_ingredients(ingredients)

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

	def parse_sodexo_dietary_restrictions(self, info_dict):
		for key, value in info_dict.items():
			if key in sodexo_dietary_restrictions and value:
				self.dietary_restrictions.append(key)

			elif key == 'allergens':
				for allergen in value:
					self.dietary_restrictions.append(allergen['name'].lower())

	def parse_po_nutrition_facts(self, nutrition_facts):
		self.add_po_serving_size(nutrition_facts)

		for fact_text in nutrition_facts[1:]:
			fact_list = re.split(r'\(|\):', fact_text)
			
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

	def parse_po_ingredients(self, ingredients):
		if ingredients:
			# remove 'ingredients: ' and anything else in parenthesis
			ingredients = re.sub(r'\(.*\)', '', ingredients[13:])

			for ingredient in ingredients:
				cleaned_ingredient = (
					ingredient.lower()
					.replace(' .', '')
					.replace(':', '')
					.replace('added to preserve color', '')
					.replace('added to promote color', '')
					.replace('added as a whipping agent', '')
					.replace('contains ', '')
					.replace('less than ', '')
					.replace('two percent', '')
					.replace('2%', '')
					.replace('1%', '')
					.replace('or less', '')
					.replace('each of the following', '')
					.strip()
				)

				cleaned_ingredient = re.sub('^and |^of ', '', cleaned_ingredient)
				if cleaned_ingredient:
					self.ingredients.add(cleaned_ingredient)

	def save(self, dining_hall):
		self.dish, _ = Dish.objects.get_or_create(name=self.name, dining_hall=dining_hall)

		nutrition_fact_records = self.save_nutrition_facts()
		self.save_dietary_restrictions()

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

	def save_dietary_restrictions(self):
		for name in self.dietary_restrictions:
			dietary_restriction, _ = DietaryRestrictions.objects.get_or_create(name=name)
			DietaryRestrictionsOfDish.objects.get_or_create(
				dish=self.dish,
				dietary_restriction=dietary_restriction,
			)

	def __str__(self):
		return (
			f"\t - {self.name}\n\t\t* " + 
			"\n\t\t* ".join([str(fact) for fact in self.nutrition_facts]) +
			"\n\t\t\t> " +
			"\n\t\t\t> ".join([str(ingredient) for ingredient in self.ingredients])
		)
