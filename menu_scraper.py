import requests 
from datetime import datetime

if __name__ == '__main__':

	menu_data = requests.get('https://legacy.cafebonappetit.com/api/2/menus?cafe=50').json()

	food_id_to_items = menu_data['items']

	for day in menu_data['days']:
		all_meals = day['cafes']['50']['dayparts'][0]

		for meal in all_meals:
			meal_type = meal['label']

			start_time = datetime.strptime(meal['starttime'], "%H:%M").strftime("%I:%M %p").strip('0')
			end_time = datetime.strptime(meal['endtime'], "%H:%M").strftime("%I:%M %p").strip('0')
			hours = f"{start_time} - {end_time}"

			stations = meal['stations']

			for station in stations:
				station_name = station['label']
				food_ids = station['items']
				
				for food_id in food_ids:
					food_name = food_id_to_items[food_id]['label']
					print(food_id_to_items[food_id])