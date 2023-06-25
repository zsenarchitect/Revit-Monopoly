from __future__ import print_function
#!/usr/bin/python
# -*- coding: utf-8 -*-
import traceback
import os
"""
import logging

logging.basicConfig(level=logging.DEBUG,
                    filemode="w",
                    filename="{}\MAIN ERROR_log.txt".format(os.path.dirname(os.path.realpath(__file__))))
"""

def try_catch_error(func):

    def wrapper(*args, **kwargs):

        #print_note ("Wrapper func for EA Log -- Begin: {}".format(func.__name__))
        try:
            # print "main in wrapper"
            out = func(*args, **kwargs)
            #print_note ( "Wrapper func for EA Log -- Finish:")
            return out
        except Exception as e:
            print_note (  "Wrapper func for EA Log -- Error: " + str(e)  )
            error = traceback.format_exc()
            print_note (error)
            
            error += "\n\n######If you have EnneadTab UI window open, just close the window. Do no more action, otherwise the program might crash.##########\n#########Not sure what to do? Msg Sen Zhang, you have dicovered a important bug and we need to fix it ASAP!!!!!########"
            error_file = "{}\local_error_log.txt".format(os.path.dirname(os.path.realpath(__file__)))
            with open(error_file, "w") as f:
                f.write(error)
            os.startfile(error_file)
            


    return wrapper


def print_note(string):
    string = str(string)
    show_note = True
    if show_note:
        try:
            #from pyrevit import script
          
            script.get_output().print_md( "***[DEBUG NOTE]***:{}".format(string))
        except Exception as e:

            print ("[DEBUG NOTE]:{}".format(string))
            # print "--Cannot use markdown becasue: {}".format(e)
