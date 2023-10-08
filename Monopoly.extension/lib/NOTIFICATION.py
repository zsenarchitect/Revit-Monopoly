import os




def run_exe():
    # script parrent folder
    lib_folder = os.path.dirname(os.path.abspath(__file__))
    # print lib_folder
    extension_folder = os.path.dirname(lib_folder)
    # print extension_folder
    exe_file_path = r"{}\bin\EXE\Monopoly_Popup\POPUP.exe".format(extension_folder)   
    # print exe_file_path
    os.startfile(exe_file_path)