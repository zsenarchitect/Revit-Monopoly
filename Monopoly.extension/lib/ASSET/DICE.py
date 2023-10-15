# give random number. or use special dice.

# it is affected by th luck of player

import random
from ASSET import Asset
import SOUND
from pyrevit import forms
import NOTIFICATION
import os


class Dice(Asset):
    pass


    def roll(self, luck):
        """return random integer between 1 and 6"""
        SOUND.roll_dice()
        
        
        while True:
            num =  random.randint(1, 15) 
            """
            num = int (num * ((luck + 50)/100) )
            if luck > 70 and num <= 1:
                continue
                
            if luck < 30 and abs(num) >= 3:
                continue

            if luck >30 and num == 0:
                continue
            """
            break

        forms.toast("Dice = {}".format(num), title="Player {}'s Dice".format(self.player_name),  icon=self.icon_path, appid = "Monopoly")
        NOTIFICATION.pop_msg("Dice = {}".format(num))
        SOUND.speak("Player {} get {} on dice".format(self.player_name, num))
        
        self.last_roll = num
        return num
    

    @property
    def icon_path(self):
        root_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        icon_path = "{}\\bin\\icon\\dice.png".format(root_folder)
        #print (icon_path)
        return icon_path
    
        return os.path.join(os.path.dirname(__file__), "dice.png")


