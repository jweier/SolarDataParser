class Day:

    def __init__(self):
        self.January = []
        self.February = []
        
    def create_day(self, date, solar_energy_exported, grid_energy_imported, grid_energy_exported_from_solar, consumer_energy_imported_from_grid, consumer_energy_imported_from_solar):
        self.date = date
        self.solar_energy_exported = solar_energy_exported
        self.grid_energy_imported = grid_energy_imported
        self.grid_energy_exported_from_solar = grid_energy_exported_from_solar
        self.consumer_energy_imported_from_grid = consumer_energy_imported_from_grid
        self.consumer_energy_imported_from_solar = consumer_energy_imported_from_solar

class Month:

    January = []
    February = []

    def __init__(self):
        self.January = []
        self.February = []

    

    