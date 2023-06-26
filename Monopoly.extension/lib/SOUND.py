"""handle all sound"""
import os
from System.Media import SoundPlayer

def play_sound(sound_file):
    """play sound"""

    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sound_file_path = "{}\\bin\\audio\\{}".format(root_folder, sound_file)

    #print "sound_file_path = " + sound_file_path


    #print "final path = " + path

    
    sp = SoundPlayer()
    sp.SoundLocation = sound_file_path
    sp.Play()



def player_moving():
    """play sound when player move"""
    play_sound("sound effect_mario jump.wav")

def player_bankrupted():
    """play sound when player is bankrupted"""
    pass

def player_won():
    """play sound when player won"""
    pass

def money_transaction():
    """play sound when money transaction"""
    pass

def construction():
    """play sound when player build a building, upgrade or downgrade a property."""
    pass



def jail_enter():
    """play sound when player enter jail, this is plice car alarm"""
    pass

def jail_leave():
    """play sound when player leave jail"""
    pass

def hospital_enter():
    """play sound when player enter hospital, this is ambulance alarm"""
    pass

def hospital_leave():
    """play sound when player leave hospital"""
    pass

def roll_dice():
    """play sound when player roll dice"""
    play_sound("sound effect_dice.wav")

def game_over():
    """play sound when game over"""
    play_sound("sound effect_game over.wav")


def read_card_description():
    """TTS when read card description"""
    pass

def show_card_happy():
    """play sound when show card with good event"""
    pass

def show_card_unhappy():
    """play sound when show card with bad event"""
    pass

def menu_flip_left():
    """play sound when menu flip left"""
    pass

def menu_flip_right():
    """play sound when menu flip right"""
    pass

def menu_select():
    """play sound when menu select"""
    pass

