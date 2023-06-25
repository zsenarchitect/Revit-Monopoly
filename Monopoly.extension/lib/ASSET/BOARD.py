
import BUILDING



from ASSET import Asset
import FINDER

class Board(Asset):
    """Inherate from Asset
    this handle the map baord itself. There is one map, each position on map is a abstract marker object
    
    
    For furture, can use design option as map control, so in one revit file there can be many level to play from."""
    
    def __init__(self):
        """this is a contructor of board
        Args:
        not args"""
        
        birth_place = BUILDING.BIRTH_PLACE.BirthPlace()
        gate = BUILDING.GATE.Gate()
        hospital = BUILDING.HOSPITAL.Hospital() 
        jail = BUILDING.JAIL.Jail()
        train_station_A = BUILDING.TRAIN_STATION.TrainStation("A")
        train_station_B = BUILDING.TRAIN_STATION.TrainStation("B")
        store = BUILDING.STORE.Store()


        # dict for key position index
        self.map_key = {
            -1: birth_place,
            0: gate,
            -10: hospital,
            -100: jail,
            -1000: train_station_A,
            -1001: train_station_B,
            -2000: store
        }

        avaiable_route_indexs = self.find_all_route_index()
        for index in avaiable_route_indexs:
            self.map_key[index] = FINDER.get_abstract_marker_by_index(index)

        self.update_file_position_index()



    def find_all_route_index(self):
        """find all abstract mark that is part of mapin file, return the sorted list of index
        """
        pass


    def update_file_position_index(self):
        """for each item map, make sure the revit object parameter for position index is matching the map_key dict"""
        pass


