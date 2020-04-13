import json
import sys
import time
import datetime
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fivecbites.settings")
django.setup()

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from station import Station
from menu import Menu
from food_item import FoodItem


class MenuScraper:

	# name, (school, cafe_id)
	bon_appetit_dict = {
		"collins": ("claremont mckenna", "50"),
		"mcconnell": ("pitzer", "219"),
	}

	# name, (school, menu_id, location_id)
	sodexo_dict = {
		"hoch-shanahan": ("harvey mudd", "15258", "13147001"),
		"malott": ("scripps", "15245", "10638001")
	}

	pomona_dining_halls = [
		"frary",
		"frank",
		"oldenborg"
	]

	def __init__(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		
		platform = sys.platform if sys.platform == 'linux' else 'mac'

		self.driver = webdriver.Chrome(
			options=options, 
			executable_path=f'{os.path.abspath(os.getcwd())}/chromedriver_{platform}'
		)

		self.menus = []

	def run(self):
		# self.scrape_bon_appetite_menus()
		self.scrape_sodexo_menus()
		# self.scrape_pomona_menus()
		self.close_driver()
		# self.print_menus()
		self.save_menus()

	def scrape_bon_appetite_menus(self):
		for cafe_name, (school, cafe_id) in MenuScraper.bon_appetit_dict.items():
			url = f"https://legacy.cafebonappetit.com/api/2/menus?cafe={cafe_id}"
			self.driver.get(url)
			menu_data = json.loads(self.driver.find_element_by_tag_name("pre").text)

			food_id_to_items = menu_data['items']

			for day in menu_data['days']:

				all_meals = day['cafes'][cafe_id]['dayparts'][0]

				for meal in all_meals:
					start_time = datetime.strptime(meal['starttime'],  "%Y-%m-%dT%H:%M:%S")
					end_time = datetime.strptime(meal['starttime'],  "%Y-%m-%dT%H:%M:%S")

					menu = Menu(cafe_name, meal['label'], start_time, end_time, None)

					stations = meal['stations']

					for station in stations:
						menu_station = Station(station['label'])
						
						for food_id in station['items']:
							food_item = FoodItem(
								name=food_id_to_items[food_id]['label'],
								dining_hall='bon appetite',
								nutrition_facts=food_id_to_items[food_id]['nutrition_details'],
								ingredients=None,
							)
							menu_station.add_food_item(food_item)

						menu.add_station(menu_station)

					self.menus.append(menu)

	def scrape_sodexo_menus(self):
		for cafe_name, (school, menu_id, location_id) in MenuScraper.sodexo_dict.items():
			url = f"https://menus.sodexomyway.com/BiteMenu/MenuOnly?menuid={menu_id}&locationid={location_id}"
			self.driver.get(url)

			menu_week = json.loads(self.driver.find_element_by_id('nutData').text)
			
			for menu_day in menu_week:
				day_of_week = datetime.strptime(menu_day['date'], "%Y-%m-%dT%H:%M:%S").strftime("%A")

				for meal in menu_day['dayParts']:
					meal_name = meal['dayPartName'].lower()

					start_time = None
					menu = None
					for course in meal['courses']:
						station_name = course['courseName'].replace(' SCR', '').replace('HMC ', '')
						if station_name not in ['HAVE A GREAT DAY!', 'MISC']:
							menu_station = Station(station_name)

							for menu_item in course['menuItems']:
								if not start_time:

									start_time = datetime.strptime(menu_item['startTime'], "%Y-%m-%dT%H:%M:%S")
									end_time = datetime.strptime(menu_item['endTime'], "%Y-%m-%dT%H:%M:%S")

									menu = Menu(
										cafe_name,
										meal_name,
										start_time,
										end_time,
										day_of_week
									)

								food_item = FoodItem(
									name=menu_item['formalName'],
									dining_hall='sodexo',
									nutrition_facts=menu_item,
									ingredients=None,
								)
								menu_station.add_food_item(food_item)

							menu.add_station(menu_station)
					if menu:
						self.menus.append(menu)

	def scrape_pomona_menus(self):
		for dining_hall in MenuScraper.pomona_dining_halls:
			menu = None
			url = f"https://www.pomona.edu/administration/dining/menus/{dining_hall}"
			self.driver.get(url)

			self.remove_cookie_popup()

			menu_headers = self.driver.find_elements_by_class_name('ui-accordion-header')
			menu_content = self.driver.find_elements_by_class_name('ui-accordion-content')

			for day, content in zip(menu_headers, menu_content):
				if '(CLOSED)' not in day.text:
					if day.get_attribute('aria-selected') == "false":
						actions = ActionChains(self.driver)
						actions.move_to_element(day).click().perform()
						time.sleep(.75)

					day_of_week = day.text.split(',')[0].lower()
					date = datetime.strptime(day.text.title(), "%A, %B %d, %Y")
					
					divs = content.find_elements_by_xpath(".//*[@class='nutrition-menu-section'] | .//h3 | .//h2")

					for div in divs:
						if div.tag_name == 'h2':
							meal_name = div.text.lower()

							if day_of_week in ['saturday', 'sunday'] and meal_name == 'breakfast':
								meal_name = 'brunch'

							start_time, end_time = MenuScraper.get_po_hours(dining_hall, date, day_of_week, meal_name)
							if menu and menu.get_stations():
								self.menus.append(menu)
							menu = Menu(dining_hall, meal_name, start_time, end_time, day_of_week)

						elif div.tag_name == 'h3':
							menu_station = Station(div.text)
							
						elif div.tag_name == 'div' and div.get_attribute('class') == 'nutrition-menu-section': 
							for menu_item in div.find_elements_by_class_name('menu-nutrition-item'):
								food_name = menu_item.find_element_by_class_name('nutrition-name-icons').text

								if food_name != 'TAKE OUT ONLY':
								
									try:
										menu_item.find_element_by_class_name('nutrition-btn').click()
										nutrition = menu_item.find_element_by_class_name('column-2')
										nutrition_facts = [fact.text for fact in nutrition.find_elements_by_tag_name('p')]

										ingredients = menu_item.find_element_by_tag_name('p')[-1].text
									except:
										nutrition_facts = []
										ingredients = None

									try:
										food_item = FoodItem(
											name=food_name,
											dining_hall=dining_hall,
											nutrition_facts=nutrition_facts,
											ingredients=ingredients,
										)

										menu_station.add_food_item(food_item)
									except Exception as e:
										print(food_name)
										print(e)
										exit()
							if menu_station and menu_station.get_food_items():
								menu.add_station(menu_station)

			# save final menu of each day
			if menu and menu.get_stations():
				self.menus.append(menu)

	@staticmethod
	def get_po_hours(dining_hall, date, day, meal_name):
		if dining_hall == 'frary':
			if day in ['saturday', 'sunday']:
				if meal_name == 'Breakfast':
					hours = '7:30-9:30'
				elif meal_name == 'brunch':
					hours = '10:30-13:30'
				else:
					hours = '17:00-20:00'
			else:
				if meal_name == 'breakfast':
					hours = '7:30-10:00'
				elif meal_name == 'lunch':
					hours = '11:30-14:00'
				else:
					hours = '17:00-20:00'
		elif dining_hall == 'frank':
			if day == 'sunday':
				if meal_name == 'brunch':
					hours = '11:00-13:00'
				else:
					hours = '17:30-19:00'
			else:
				if meal_name == 'breakfast':
					hours = '7:30-10:00'
				elif meal_name == 'brunch':
					hours = '11:30-13:00'
				else:
					hours = '17:00-19:00'
		else:
			hours = '12:00-13:00'

		start_time = datetime.combine(date, datetime.strptime(hours.split('-')[0], '%H:%M').time())
		end_time = datetime.combine(date, datetime.strptime(hours.split('-')[1], '%H:%M').time())
		return start_time, end_time

	def remove_cookie_popup(self):
		try:
			self.driver.find_element_by_id('cookie-policy-accepted').click()
		except:
			pass

	def print_menus(self):
		for menu in self.menus:
			print(menu)

	def save_menus(self):
		for menu in self.menus:
			menu.save()

	def close_driver(self):
		self.driver.close()


if __name__ == "__main__":
	start = time.time()

	menu_scraper = MenuScraper()
	menu_scraper.run()

	time_in_min = (time.time() - start) / 60
	print(f"total time: {time_in_min:.2f} minutes")
