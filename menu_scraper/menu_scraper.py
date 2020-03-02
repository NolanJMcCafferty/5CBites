import json
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from station import Station
from menu import Menu
from food_item import FoodItem

class MenuScraper():

	# name, cafe_id
	bon_appetit_dict = {
		'claremont mckenna': "50",
		"pitzer": "219"
	}

	# name, (menu_id, location_id)
	sodexo_dict = {
		"harvey mudd": ("15258", "13147001"),
		"scripps": ("15245", "10638001")
	}

	pomona_dining_halls = [
		"frary",
		"frank",
		"oldenborg"
	]

	def __init__(self):
		options = webdriver.ChromeOptions()
		# options.add_argument('--headless')
		
		platform = sys.platform if sys.platform == 'linux' else 'mac'
		self.driver = webdriver.Chrome(
			options=options, 
			executable_path=f'../menu_scraper/chromedriver_{platform}'
		)

		self.menus = []

	def run(self):
		# self.scrape_bon_appetite_menus()
		# self.scrape_sodexo_menus()
		self.scrape_pomona_menus()
		# self.print_menus()
		self.close_driver()
		

	def scrape_bon_appetite_menus(self):
		for cafe_name, cafe_id in MenuScraper.bon_appetit_dict.items():
			url = f"https://legacy.cafebonappetit.com/api/2/menus?cafe={cafe_id}"
			self.driver.get(url)
			menu_data = json.loads(self.driver.find_element_by_tag_name("pre").text)

			food_id_to_items = menu_data['items']

			for day in menu_data['days']:

				all_meals = day['cafes'][cafe_id]['dayparts'][0]

				for meal in all_meals:
					hours = MenuScraper.format_hours(meal['starttime'], meal['endtime'])

					menu = Menu(cafe_name, day['date'], meal['label'], hours)

					stations = meal['stations']

					for station in stations:
						menu_station = Station(station['label'])
						
						for food_id in station['items']:
							food_item = FoodItem(
								name=food_id_to_items[food_id]['label']
								# tier=int(food_id_to_items[food_id]['tier']),
							)
							menu_station.add_food_item(food_item)

						menu.add_station(menu_station)

					self.menus.append(menu)

	def scrape_sodexo_menus(self):
		for cafe_name, (menu_id, location_id) in MenuScraper.sodexo_dict.items():
			url = f"https://menus.sodexomyway.com/BiteMenu/MenuOnly?menuid={menu_id}&locationid={location_id}"
			self.driver.get(url)

			menu_week = json.loads(self.driver.find_element_by_id('nutData').text)
			
			for menu_day in menu_week:
				date = menu_day['date'].split('T')[0]
				
				for meal in menu_day['dayParts']:
					meal_name = meal['dayPartName']

					hours = None
					for course in meal['courses']:
						station_name = course['courseName'].replace(' SCR', '').replace('HMC ', '')
						menu_station = Station(station_name)

						for menu_item in course['menuItems']:
							if not hours:
								hours = MenuScraper.format_hours(
									menu_item['startTime'].split('T')[1], 
									menu_item['endTime'].split('T')[1]
								)

								menu = Menu(cafe_name, date, meal_name, hours)

							food_item = FoodItem(
								name=menu_item['formalName']
							)
							menu_station.add_food_item(food_item)

						menu.add_station(menu_station)

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
						time.sleep(.5)

					day_of_week = day.text.split(',')[0].lower()
					date = datetime.strptime(day.text.title(), "%A, %B %d, %Y").strftime("%Y-%m-%d")
					
					divs = content.find_elements_by_xpath(".//*[@class='nutrition-menu-section'] | .//h3 | .//h2")
					for div in divs:
						if div.tag_name == 'h2':
							meal_name = div.text

							if day_of_week in ['saturday', 'sunday'] and meal_name == 'Breakfast':
								meal_name = 'Brunch'

							hours = MenuScraper.get_pomona_hours(dining_hall, day_of_week, meal_name)
							if menu:
								self.menus.append(menu)
								print(menu)
							menu = Menu(dining_hall, date, meal_name, hours)
							 
						elif div.tag_name == 'h3':
							menu_station = Station(div.text)
							
						elif div.tag_name == 'div' and div.get_attribute('class') == 'nutrition-menu-section': 
							for menu_item in div.find_elements_by_class_name('menu-nutrition-item'):
								food_name = menu_item.find_element_by_class_name('nutrition-name-icons').text
								food_item = FoodItem(name=food_name)
								menu_station.add_food_item(food_item)
							menu.add_station(menu_station)

			# save final menu of each day
			self.menus.append(menu)
			print(menu)


	def get_pomona_hours(dining_hall, day, meal_name):
		if dining_hall == 'frary':
			if day in ['saturday', 'sunday']:
				if meal_name == 'Breakfast':
					hours = '7:30AM-9:30AM'
				elif meal_name == 'Brunch':
					hours = '10:30AM-1:30PM'
				else:
					hours = '5:00PM-8:00PM'
			else:
				if meal_name == 'Breakfast':
					hours = '7:30AM-10:00AM'
				elif meal_name == 'Lunch':
					hours = '11:30AM-2:00PM'
				else:
					hours = '5:00PM-8:00PM'
		elif dining_hall == 'frank':
			if day == 'sunday':
				if meal_name == 'Brunch':
					hours = '11:00AM-1:00PM'
				else:
					hours = '5:30PM-7:00PM'
			else:
				if meal_name == 'Breakfast':
					hours = '7:30AM-10:00AM'
				elif meal_name == 'Brunch':
					hours = '11:30AM-1:00PM'
				else:
					hours = '5:00PM-7:00PM'
		else:
			hours = '12:00AM-1:00PM'

		return hours

	def remove_cookie_popup(self):
		try:
			self.driver.find_element_by_id('cookie-policy-accepted').click()
		except:
			pass


	def format_hours(start_time, end_time):
		start_time = datetime.strptime(start_time, "%H:%M:%S").strftime("%I:%M %p").strip('0')
		end_time = datetime.strptime(end_time, "%H:%M:%S").strftime("%I:%M %p").strip('0')
		return f"{start_time} - {end_time}"

	def print_menus(self):
		for menu in menus:
			print(menu)

	def close_driver(self):
		self.driver.close()


if __name__ == "__main__":
	menu_scraper = MenuScraper()
	menu_scraper.run()

	
