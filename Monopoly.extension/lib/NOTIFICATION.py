import os
import json

def pop_msg(main_text):
    return
    if not main_text:
        main_text = "Quack!"


    data = {"main_text":main_text,"image":None}
    
    file_name = "DUCK_POP.json"
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
    # print lib_folder
    extension_folder = os.path.dirname(lib_folder)
    # print extension_folder
    exe_file_path = r"{}\bin\EXE\Monopoly_Popup\POPUP.exe".format(extension_folder)   
    # print exe_file_path
    os.startfile(exe_file_path)