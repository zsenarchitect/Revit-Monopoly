# if current inteprater is python 2.x then import future print function

from __future__ import print_function


import time
import pygame
import button
import traceback
import os
import math
from gtts import gTTS
import random
import pyautogui
import math
import sys
import json
import logging
logging.basicConfig(level=logging.DEBUG,
                    filename="Speaker_Error_Log.txt",
                    filemode="w")


def get_local_dump_folder():
    """get the user document folder and create a Monopoly folder inside if it does not exist, then return that Monopoly folder"""
    user_doc_folder = os.path.expanduser('X')
    monopoly_folder = "{}\Monopoly".format(user_doc_folder)

    if not os.path.exists(monopoly_folder):
        os.makedirs(monopoly_folder)

    return monopoly_folder


def try_catch_error(func):
    def wrapper(*args, **kwargs):
        try:
            out = func(*args, **kwargs)
            return out
        except Exception as e:
            error = traceback.format_exc()
            print(error)
            logging.debug(traceback.format_exc())
    return wrapper


class TTS:

    def __init__(self):
        pass

    @try_catch_error
    def speak(self, text, lang='en', accent='com'):

        tts = gTTS(text=text, lang=lang, tld=accent)
        # the save address should be in user desktop for folder access reason
        filename = "{}\TTS_{}.mp3".format(
            get_local_dump_folder(), random.random())
        tts.save(filename)

        pygame.mixer.init()
        pygame.mixer.music.set_volume(float(self.volume) / 100)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():

            pygame.time.Clock().tick(10)

        pygame.mixer.quit()

        os.remove(filename)

        return True

    def read_from_file(self):

        file_name = "Monopoly_Speaker.json"
        dump_folder = get_local_dump_folder()
        file_path = "{}\{}".format(dump_folder, file_name)

        # return false if filename not exist in dump folder, use os moudle
        if not os.path.isfile(file_path):
            return False

        # dont speak for file too old
        if time.time() - os.path.getctime(file_path) > 60 or time.time() - os.path.getmtime(file_path) > 60:

            # remove file_path from dump folder using os module
            os.remove(file_path)

            # print "old file"
            now = time.time()
            # print now
            # print now - os.path.getctime( file_path)
            # print now - os.path.getmtime( file_path)
            return False

        try:
            # read json file and return dict using json module
            with open(file_path) as f:
                data = json.load(f)

        except:
            return False
        text = data["text"]
        language = data["language"]
        accent = data["accent"]

        res = self.speak(text, language, accent)
        if res:
            # print "speak finish"

            # remove file_path from dump folder using os module
            os.remove(file_path)

            return True

        return False

    def rotate_img_around_center(self, image, rect, angle):
        """Rotate the image while keeping its center."""
        # Rotate the original image without modifying it.
        new_image = pygame.transform.rotate(image, angle)
        # Get a new rect with the center of the old rect.
        rect = new_image.get_rect(center=rect.center)
        return new_image, rect

    def get_pointer_angle(self, pt_x, pt_y):
        """get the angle of a line[current mouse position to a given pt] to X axis"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x == pt_x:
            return 90 + 180 * (mouse_y > pt_y)
        angle = math.atan(-float(mouse_y - pt_y) /
                          float(mouse_x - pt_x)) * 180 / math.pi
        angle += 180 * (mouse_x < pt_x)  # force extra rotate
        return angle

    def is_another_TTS_running(self):

        # print [x.title for x in pyautogui.getAllWindows()]
        for window in pyautogui.getAllWindows():
            # print window.title
            if window.title == u"Monopoly Talkie":
                return True
        return False

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    @try_catch_error
    def main(self):
        if self.is_another_TTS_running():
            # speak("there is another 'Monopoly Talkie' opened. Now quiting")
            # print "other TTS running"
            return

        # script_dir = os.path.abspath( os.path.dirname( __file__ ) )
        # print "A GUI designed by Sen Zhang for Ennead Architect."
        # print ("%%%%%%%%%%%%%%%%%%%%%")
        # print (script_dir)
        pygame.init()

        # create game window
        SCREEN_WIDTH = 300
        SCREEN_HEIGHT = 300

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.iconify()

        pygame.display.set_caption("Monopoly Talkie")

        # game variables
        game_paused = False
        menu_state = "main"

        # define fonts
        font_title = pygame.font.SysFont("arialblack", 30)
        font_subtitle = pygame.font.SysFont("arialblack", 20)
        font_body = pygame.font.SysFont("arial", 15)
        font_note = pygame.font.SysFont("arialblack", 10)

        # define colours
        TEXT_COL = (255, 255, 255)
        TEXT_COL_FADE = (150, 150, 150)

        # logo
        # exe_folder = r"L:\\4b_Applied Computing\\03_Rhino\\12_Monopoly for Rhino\Source Codes\lib\Monopoly_Speaker"
        
        script_folder = os.path.abspath(os.path.dirname(__file__))

        Monopoly_logo = pygame.image.load("{}\\dollar_bag.png".format(script_folder)).convert_alpha()
        target_img_size = (100, 100)
        Monopoly_logo = pygame.transform.scale(Monopoly_logo, target_img_size)
        original_logo = Monopoly_logo
        logo_rect = Monopoly_logo.get_rect(center=(100, SCREEN_HEIGHT - 100))
        angle = 0

        # Clock
        clock = pygame.time.Clock()
        FPS = 30

        self.volume = 20

        # load button images
        # mute_img = pygame.image.load("images\\button_audio_mute.png").convert_alpha()
        # unmute_img = pygame.image.load("images\\button_audio_unmute.png").convert_alpha()
        # louder_img = pygame.image.load("images\\button_audio_higher_voice.png").convert_alpha()
        # quieter_img = pygame.image.load("images\\button_audio_lower_voice.png").convert_alpha()
        quit_img = pygame.image.load("{}\\button_quit.png".format(script_folder)).convert_alpha()
        # coffin_img = pygame.image.load("images\\button_coffin.png").convert_alpha()

        # create button instances
        # mute_button = button.Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, mute_img, 1)
        # unmute_button = button.Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, unmute_img, 1)
        # kill_button = button.Button(60, SCREEN_HEIGHT/2 + 50, coffin_img, 0.2)

        # louder_button = button.Button(SCREEN_WIDTH/2, SCREEN_HEIGHT - 200, louder_img, 0.7)
        # quiter_button = button.Button(SCREEN_WIDTH/2 + 170, SCREEN_HEIGHT - 200, quieter_img, 0.7)
        quit_button = button.Button(
            SCREEN_WIDTH/2, SCREEN_HEIGHT - 140, quit_img, 1)

        # game loop
        run = True
        is_mute = False
        life_max = 60 * 60 * FPS  # 60mins x FPS
        life_count = life_max
        while run:
            self.screen.fill((176, 121, 72))

            # self.draw_text("Click on coffin to never hear her again.", font_note, TEXT_COL, 50, SCREEN_HEIGHT/2 + 100)
            # if kill_button.draw(self.screen):
            #     self.speak("Gentlemen, it has been a privilege playing with you tonight.")
            #     self.mark_kill_file()
            #     run = False
            #     break

            if not is_mute:
                res = self.read_from_file()
                if res:
                    life_count = life_max

            # this is to keep it facing mouse
            angle = self.get_pointer_angle(*logo_rect.center)
            Monopoly_logo, logo_rect = self.rotate_img_around_center(
                original_logo, logo_rect, angle)
            self.screen.blit(Monopoly_logo, logo_rect)

            # check if game is paused
            self.draw_text("Monopoly.", font_title, TEXT_COL, 50, 50)
            # self.draw_text("Keep this window alive. ", font_title, TEXT_COL_FADE, 50, 100)
            # self.draw_text("Do not close after every talk.", font_title, TEXT_COL_FADE, 50, 130)
            # self.draw_text("Minimize it is ok though.", font_title, TEXT_COL_FADE, 50, 160)

            # self.draw_text("So other tools keep broadcast messages without initiating talkie", font, TEXT_COL_FADE, 50, 200)
            # self.draw_text("over and over again. Every initiation takes a few seconds, so let's", font, TEXT_COL_FADE, 50, 230)
            # self.draw_text("initiate as few times as possible.", font, TEXT_COL_FADE, 50, 260)

            # if is_mute:
            #     self.draw_text("Currently Muted.", font_subtitle, TEXT_COL, 50, SCREEN_HEIGHT/2)
            #     if unmute_button.draw(self.screen):
            #         is_mute = not is_mute
            #         self.speak("Thank God! I can talk again.")
            #         life_count = life_max
            # else:
            #     self.draw_text("Currently Talky.", font_subtitle, TEXT_COL, 50, SCREEN_HEIGHT/2)
            #     if mute_button.draw(self.screen):
            #         is_mute = not is_mute
            #         self.speak("Ok, I will not talk to you anymore!")

            # if louder_button.draw(self.screen):
            #     self.volume = min(self.volume + 10, 100)
            #     self.speak("Increasing voice level.")

            # if quiter_button.draw(self.screen):
            #     self.volume = max(self.volume - 10, 0)
            #     self.speak("Decreasing voice level.")

            # self.draw_text("Voice Volume = {}. (Range 0~100)".format(self.volume), font_note, TEXT_COL, SCREEN_WIDTH/2, SCREEN_HEIGHT - 220)

            if quit_button.draw(self.screen):
                run = False

            if life_count < 0:
                run = False
            text_life = int(life_count / FPS)
            text_min = int(math.floor(text_life / 60))
            text_secs = text_life % 60
            self.draw_text("Monopoly Talkie will close itself", font_note, TEXT_COL, 50, SCREEN_HEIGHT - 40)
            self.draw_text("in {}m {}s if there is nothing to say.".format(
                text_min, text_secs), font_note, TEXT_COL, 50, SCREEN_HEIGHT - 20)
            life_count -= 1

            # event handler
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_paused = True
                if event.type == pygame.QUIT:
                    run = False

            clock.tick(FPS)
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":

    TTS().main()
