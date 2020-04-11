from hello.models import MenuItem


class Station:

	def __init__(self, name):
		self.name = name
		self.food_items = []

	def add_food_item(self, food_item):
		self.food_items.append(food_item)

	def get_food_items(self):
		return self.food_items

	def save(self, meal):
		nutrition_fact_records = []
		for food_item in self.food_items:
			dish, nf_records = food_item.save(meal.dining_hall)
			nutrition_fact_records += nf_records
			menu_item, _ = MenuItem.objects.get_or_create(
				meal=meal,
				dish=dish,
				station=self.name
			)

		return nutrition_fact_records

	def __str__(self):
		return (
			f"\n{self.name}\n" +
			"\n".join([str(food_item) for food_item in self.food_items])
		)