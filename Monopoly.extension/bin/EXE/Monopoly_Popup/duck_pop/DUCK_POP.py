"""compile this using small laptop py 3.10 run compiuler"""
import traceback
import os


    
    
    
try:

    import tkinter as tk
    import time
    import math
    from tkinter import ttk
    from PIL import Image as pim
    
except:
    error = traceback.format_exc()

    error += "\n\n######If you have EnneadTab UI window open, just close the window. Do no more action, otherwise the program might crash.##########\n#########Not sure what to do? Msg Sen Zhang, you have dicovered a important bug and we need to fix it ASAP!!!!!########"
    error_file = "{}\Documents\EnneadTab Settings\Local Copy Dump\error_log.txt".format(
        os.environ["USERPROFILE"])
    print (error)

    with open(error_file, "w") as f:
        f.write(error)
    os.startfile(error_file)




def try_catch_error(func):

    def wrapper(*args, **kwargs):

        # print_note ("Wrapper func for EA Log -- Begin: {}".format(func.__name__))
        try:
            # print "main in wrapper"
            out = func(*args, **kwargs)
            # print_note ( "Wrapper func for EA Log -- Finish:")
            return out
        except Exception as e:
            # print(str(e))
            # print("Wrapper func for EA Log -- Error: " + str(e))
            error = traceback.format_exc()

            error += "\n\n######If you have EnneadTab UI window open, just close the window. Do no more action, otherwise the program might crash.##########\n#########Not sure what to do? Msg Sen Zhang, you have dicovered a important bug and we need to fix it ASAP!!!!!########"
            error_file = "{}\Documents\EnneadTab Settings\Local Copy Dump\error_log.txt".format(
                os.environ["USERPROFILE"])

            with open(error_file, "w") as f:
                f.write(error)
            os.startfile(error_file)

    return wrapper



def get_file_in_dump_folder( file):
    return "{}\Documents\EnneadTab Settings\Local Copy Dump\{}".format(os.environ["USERPROFILE"], file)

def read_json_as_dict_in_dump_folder(file):
    filepath = get_file_in_dump_folder(file)
    
    # return empty dict if file not exist
    if not os.path.exists(filepath):
        return {}
    import json
    # reads it back
    with open(filepath,"r") as f:
      dict = json.load(f)
    return dict

def fake_test_data():
    filepath = get_file_in_dump_folder("DUCK_POP.json")
    

    import json
    
    dict = {"main_text":"Hello Human!!",
            "image":None}
    
    with open(filepath,"w") as f:
      json.dump(dict, f)



class DuckPopApp:
    @try_catch_error
    def __init__(self, text,
                 animation_in_duration,
                 animation_stay_duration,
                 animation_fade_duration,
                 width,
                 height,
                 image):

        self.window = tk.Tk()
        self.window.iconify()
        # self.window.title("EnneadTab Messager")

        # self.window.attributes("-topmost", True)
        self.window.deiconify()
        self.begining_time = time.time()

        self.window_width = width
        self.window_height = height
        # self.x = self.get_screen_width() // 2 - self.window_width//2
        self.x = -500
        self.y_final = self.get_screen_height() - self.window_height+250
        self.y_initial = self.get_screen_height()
        self.iteration = 0

        # 100x100 size window, location 700, 500. No space between + and numbers
        self.window.geometry("{}x{}+{}+{}".format(self.window_width,
                                                  self.window_height,
                                                  self.x,
                                                  self.y_initial))

        self.style = ttk.Style()
        self.style.configure(
            "Rounded.TLabel",
            background="dark grey",
            borderwidth=6,
            # relief="solid",
            foreground="white",
            font=("Comic Sans MS", 20),
            outline="white",
            bordercolor="orange",
            padding=20,
            anchor="center",
        )

        self.talk_bubble = ttk.Label(
            self.window, text=text, style="Rounded.TLabel"
        )
        # pady ====> pad in Y direction
        self.talk_bubble.pack(pady=5)

        image = "L:\\4b_Applied Computing\\01_Revit\\04_Tools\\08_EA Extensions\\Published\\ENNEAD.extension\\Ennead.tab\\Utility.panel\\exe_2.stack\\duck_pop\\duck_small.png"

        # print (image)
        # from PIL import Image
 
        # # open the original image
        # original_img = Image.open(image)
        
        # # Flip the original image vertically
        # flip_image = original_img.transpose(method=Image.FLIP_LEFT_RIGHT)

        # load jpg by tk.photoimage
        self.image = tk.PhotoImage(file = image, format="PNG")
        # flip image left to right
        self.image_bubble = tk.Label(self.window, image = self.image, bd = 0, cursor="target")
        self.image_bubble.bind("<Button-1>", self.click_image)
        self.image_bubble.pack(padx =50)


        # set the window to have transparent background, only show the label
        self.window.config(background="green")
        self.window.wm_attributes('-transparentcolor', 'green')
        self.window.wm_attributes('-topmost', True)
        self.window.overrideredirect(True)

        self.animation_in_duration = animation_in_duration  # Animation duration in seconds
        # Time to stay visible in seconds
        self.animation_stay_duration = animation_stay_duration
        self.animation_fade_duration = animation_fade_duration  # Fade duration in seconds

        
        self.window.after(1, self.update)
        
        
    def count_frames_in_gif(self, file_path):
        frame_count = 0
        try:
            with pim.open(file_path) as img:
                while True:
                    frame_count += 1
                    try:
                        img.seek(frame_count)
                    except EOFError:
                        break
        except FileNotFoundError:
            pass
            #print("The file {} could not be found.".format(file_path))
        return frame_count
    
    def click_image(self, event):
        explosion_gif = "L:\\4b_Applied Computing\\01_Revit\\04_Tools\\08_EA Extensions\\Published\\ENNEAD.extension\\Ennead.tab\\Utility.panel\\exe_2.stack\\duck_pop\\explosion.gif"
        self.max_frame = self.count_frames_in_gif(explosion_gif)
        print (self.max_frame)
        self.frames = [tk.PhotoImage(file = explosion_gif, 
                                     format = 'gif -index %i' % (i)) for i in range(self.max_frame)]
        self.cycle_animation_frame_index = 0
        
        self.talk_bubble.pack_forget()
        self.image_bubble.pack_forget()

        
        
        self.window.geometry("{}x{}+{}+{}".format(self.window_width,
                                                      self.window_height,
                                                      self.x,
                                                      self.y_final-1500))
        self.explosition_label = tk.Label(self.window,  bd=0, bg='green')
        self.explosition_label.pack(pady=5)
        
        self.update_explosion()
        

        
    def update_explosion(self):
        self.explosition_label.configure(image=self.frames[self.cycle_animation_frame_index])
        if self.cycle_animation_frame_index == self.max_frame - 1:
            print ("FINISH")
            print(self.cycle_animation_frame_index)
            print (self.max_frame)
            self.window.destroy()
            try:
                self.quack()
            except:
                pass
            return
        self.cycle_animation_frame_index += 1
        
        # print (self.cycle_animation_frame_index)
        self.window.after(50, self.update_explosion)

    def quack(self):
        audio_folder = "L:\\4b_Applied Computing\\01_Revit\\04_Tools\\08_EA Extensions\\Published\\ENNEAD.extension\\Ennead.tab\\Utility.panel\\exe_2.stack\\duck_pop\\audio"
        import random
        # pick a random duck sound from the folder
        duck_sound_list = os.listdir(audio_folder)
        audio = os.path.join(audio_folder,random.choice(duck_sound_list))
        import sys
        sys.path.append(r"L:\\4b_Applied Computing\\03_Rhino\\12_EnneadTab for Rhino\\Dependency Modules")
        import playsound
        playsound.playsound(audio)

    @try_catch_error
    def update(self):
        # kill the app if running for more than total s .
        time_passed = time.time() - self.begining_time
        # print(time_passed)
        if time_passed > (self.animation_in_duration + self.animation_stay_duration + self.animation_fade_duration + 2) and self.x > self.get_screen_width()*2 + 20:
            self.window.destroy()
            print ("killed")
            try:
                self.quack()
            except:
                pass
            

            return

        if time_passed < self.animation_in_duration:
            progress = time_passed / self.animation_in_duration
            eased_progress = 1 - math.pow(1 - progress, 4)  # Ease-out function
            y = int(self.y_initial - eased_progress *(self.y_initial - self.y_final))
            if self.iteration % 5 == 0:
                self.x+=1
            self.window.geometry("{}x{}+{}+{}".format(self.window_width,
                                                      self.window_height,
                                                      self.x,
                                                      y))
            # print (y)

        elif time_passed > self.animation_in_duration + self.animation_stay_duration:
            progress = (time_passed - self.animation_in_duration -
                        self.animation_stay_duration) / self.animation_fade_duration   
            # print (progress)
            # if progress > 1:
            #     progress = 1        
            eased_progress = 1 - math.pow(1 - progress, 4)  # Ease-out function
            # print( 100*math.sin( 50*progress))
            if eased_progress<- 1.5:
                eased_progress = -1.5
            y = int(self.y_final + 10*math.sin(100* progress) + 100*eased_progress )

            if self.iteration % 5 == 0:
                self.x+=2
            self.window.geometry("{}x{}+{}+{}".format(self.window_width,
                                                      self.window_height,
                                                      self.x,
                                                      y))

            # print (y)
            # print ("fade")
        self.window.after(1, self.update)
        self.iteration += 1

    def run(self):
        self.window.mainloop()

    def get_screen_width(self):
        return self.window.winfo_screenwidth()

    def get_screen_height(self):
        return self.window.winfo_screenheight()

@try_catch_error
def pop_message():
    print ("working")
    INTERNAL_TEST = False
    if INTERNAL_TEST:
        fake_test_data()
    
    
    data = read_json_as_dict_in_dump_folder("DUCK_POP.json")
    if data is None or "main_text" not in data.keys():
        print ("Nothing")
        return
    
    app = DuckPopApp(text = data["main_text"],
                     animation_in_duration = data.get("animation_in_duration", 0.5),
                     animation_stay_duration = data.get("animation_stay_duration",2),
                     animation_fade_duration = data.get("animation_fade_duration", 5),
                     width = data.get("width", 1200),
                     height = data.get("height", 700),
                     image = data.get("image", None))
    app.run()
    
    if os.path.exists(get_file_in_dump_folder("DUCK_POP.json")):
        
        os.remove(get_file_in_dump_folder("DUCK_POP.json"))

    print ("done")

########################################
if __name__ == "__main__":
    pop_message()
