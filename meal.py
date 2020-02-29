
class Meal():
	
	def __init__(self, title, hours):
		self.title = title
		self.hours = hours
		self.stations = []


	def add_station(self, station):
		self.stations.append(station)

	def __str__(self):
		return (
			f"\n\n{self.title}: {self.hours}\n" + 
			"\n".join([str(station) for station in self.stations])
		)