
class Menu():

	def __init__(self, dining_hall, date, meal, hours):
		self.dining_hall = dining_hall
		self.date = date
		self.meal = meal
		self.hours = hours
		self.stations = []

	def add_station(self, station):
		self.stations.append(station)

	def __str__(self):
		return (
			f"\n\n{self.dining_hall} | {self.date} | {self.meal} | {self.hours}\n" + 
			"\n".join([str(station) for station in self.stations])
		)




