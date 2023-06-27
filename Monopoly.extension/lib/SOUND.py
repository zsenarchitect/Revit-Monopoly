"""handle all sound"""
import os
from System.Media import SoundPlayer
import json

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



def speak(text, language='en', accent='com'):
    """
    #language = 'zh-CN'
    #language = 'zh-TW'
    #language = 'en'

    #accent = 'co.uk'
    #accent = 'co.in'
    #accent = 'com'
    """
 

    if text:
        data = dict()
        data["text"] = text
        data["language"] = language
        data["accent"] = accent
        file_name = "Monopoly_Speaker.json"
        user_doc_folder =  "{}\Documents".format(os.environ["USERPROFILE"])
        
        monopoly_folder = "{}\Monopoly".format(user_doc_folder)

        if not os.path.exists(monopoly_folder):
            os.makedirs(monopoly_folder)


        file_path = os.path.join(monopoly_folder, file_name)
        with open(file_path, 'w') as f:
            json.dump(data, f)



    run_exe()

def run_exe():
    # script parrent folder
    lib_folder = os.path.dirname(os.path.abspath(__file__))
    bin_folder = os.path.dirname(lib_folder)
    exe_file_path = r"{}\EXE\Monopoly_Speaker\Monopoly_Speaker.exe - Shortcut".format(bin_folder)   
    os.startfile(exe_file_path)