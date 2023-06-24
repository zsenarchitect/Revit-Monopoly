
import BUILDING



from ASSET import Asset


class Board(Asset):
    """Inherate from Asset
    this handle the map baord itself. There is one map, each position on map is a abstract marker object
    
    
    For furture, can use design option as map control, so in one revit file there can be many level to play from."""
    
    def __init__(self):
        
        birth_place = BUILDING.BIRTH_PLACE.BirthPlace()
        gate = BUILDING.GATE.Gate()
        hospital = BUILDING.HOSPITAL.Hospital() 
        jail = BUILDING.JAIL.Jail()
        train_station_A = BUILDING.TRAIN_STATION.TrainStation("A")
        train_station_B = BUILDING.TRAIN_STATION.TrainStation("B")


        # dict for key position index
        self.map_key = {
            -1: birth_place,
            0: gate,
            -10: hospital,
            -100: jail,
            -1000: train_station_A,
            -1001: train_station_B
        }

        avaiable_route_indexs = self.find_all_route_index()



    def find_all_route_index(self):
        """find all abstract mark that is part of mapin file, return the sorted list of index
        """
        pass


