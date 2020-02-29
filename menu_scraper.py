import requests 
from datetime import datetime
from station import Station
from meal import Meal
from menu import Menu


if __name__ == '__main__':

	menu_data = requests.get('https://legacy.cafebonappetit.com/api/2/menus?cafe=50').json()

	food_id_to_items = menu_data['items']

	for day in menu_data['days']:
		menu = Menu('claremont mckenna', day['date'])

		all_meals = day['cafes']['50']['dayparts'][0]

		for meal in all_meals:
			start_time = datetime.strptime(meal['starttime'], "%H:%M").strftime("%I:%M %p").strip('0')
			end_time = datetime.strptime(meal['endtime'], "%H:%M").strftime("%I:%M %p").strip('0')
			hours = f"{start_time} - {end_time}"

			menu_meal = Meal(meal['label'], hours)

			stations = meal['stations']

			for station in stations:
				menu_station = Station(station['label'])
				
				for food_id in station['items']:
					print(food_id_to_items[food_id]['tier'])
					# if food_id_to_items[food_id]['tier'] == 1:  
					# 	food = food_id_to_items[food_id]['label']
					# 	menu_station.add_food_item(food)
					if food_id_to_items[food_id]['tier'] == 2:  
						food = '- ' + food_id_to_items[food_id]['label'] + ' ----'
						menu_station.add_food_item(food)
					# else:
					# 	food = '---- ' + food_id_to_items[food_id]['label'] + ' ----'
					# 	menu_station.add_food_item(food)

				menu_meal.add_station(menu_station)

			menu.add_meal(menu_meal)

		print(menu)


