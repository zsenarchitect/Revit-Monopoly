import logging
import ERROR_HANDLE
import os
logging.basicConfig(level=logging.INFO,
                    filename="{}\{}_log.txt".format(ERROR_HANDLE.LOG_FOLDER,
                                                    os.path.basename(__file__).rstrip(".py")),
                    filemode="w")

import BUILDING



from ASSET import Asset
from ABSTRACT_MARKER import AbstractMarker
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
        #train_station_A = BUILDING.TRAIN_STATION.TrainStation("A")
        #train_station_B = BUILDING.TRAIN_STATION.TrainStation("B")
        #store = BUILDING.STORE.Store()


        # dict for key position index
        self.map_key = {
            -1: birth_place,
            0: gate,
            -10: hospital,
            -11: jail#,
            #-12: train_station_A,
            #-13: train_station_B,
            #-14: store
        }

        abstract_marker_instances = [x for x in FINDER.get_all_generic_models() if x.Symbol.Family.Name == "AbstractMarker"]
        for abstract_marker_instance in abstract_marker_instances:
            abstract_marker = AbstractMarker(abstract_marker_instance)
            self.map_key[abstract_marker.position_index] = abstract_marker
          
        #print (self.map_key)
        #self.update_file_position_index()






    def update_file_position_index(self):
        """for each item map, make sure the revit object parameter for position index is matching the map_key dict"""
        
        
        for index, asset in self.map_key.items():
            print (index)
            logging.info("updating position index for {} to {}".format(asset.revit_object, index))
            asset.update_position_index(index)

    @property
    def max_marker_index(self):
        """return the max index of marker"""
        return max(self.map_key.keys())