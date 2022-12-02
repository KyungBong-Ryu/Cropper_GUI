import os

import tkinter as tki
from tkinter.colorchooser import askcolor

from PIL import Image


from utils import *

_blank =  "                                                                                                    "
_blank += "                                                                                                    "

_line_solid =  " ______________________________________________________________"
_line_solid += "______________________________________________________________ "

_line_dash =  " _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  "
_line_dash += "_  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _ "

def get_main_path():
    global tk_1_entry_path, _path, tk_1_label_curr_path_info, _list
    
    try:
        _path = str(tk_1_entry_path.get())
        _path = _path.replace("\\", "/")
        while _path[-1] == '/':
            _path = _path[:-1]

        try:
            _list = load_file_list(_path)
            print(_list)
        except:
            _path = "Wrong path: file list update FAIL"
    except:
        #print("input error")
        _path = "Wrong path: input error"


    tk_1_label_curr_path_info = tki.Label(tk_main, text=_blank, bg='white').grid(row=1, column=1)
    tk_1_label_curr_path_info = tki.Label(tk_main, text=_path, bg='white').grid(row=1, column=1)

    #print(_path)
    #print(_list)


def show_sample_image():
    global _path, _list
    try:
        pil_sample = Image.open(_path + '/' + _list[0]).convert('RGB')
        imshow_pil(pil_sample)
    except:
        pass

def get_crop_coor():
    global _coor_ul_w, _coor_ul_h, _coor_dr_w, _coor_dr_h
    try:
        _coor_ul_w = int(tk_1_entry_coor_up_left_w.get())
        _coor_ul_h = int(tk_1_entry_coor_up_left_h.get())
        _coor_dr_w = int(tk_1_entry_coor_down_right_w.get())
        _coor_dr_h = int(tk_1_entry_coor_down_right_h.get())
    except:
        _coor_ul_w = int(0)
        _coor_ul_h = int(0)
        _coor_dr_w = int(0)
        _coor_dr_h = int(0)

    _str = "Crop Coor (w,h): Up Left (" + str(_coor_ul_w) + ", " + str(_coor_ul_h) + "), Down Right (" + str(_coor_dr_w) + ", " + str(_coor_dr_h) + ")"
    #print(_str)
    
    tk_1_label_curr_coor_info = tki.Label(tk_main, text=_blank, bg='white').grid(row=3, column=1)
    tk_1_label_curr_coor_info = tki.Label(tk_main, text=_str, bg='white').grid(row=3, column=1)

def show_crop_sample_image():
    global _path, _list, _coor_ul_w, _coor_ul_h, _coor_dr_w, _coor_dr_h
    global _line_color_string, _line_solid_dash, _line_thickness, _dash_length, _dash_interval
    try:
        pil_sample = Image.open(_path + '/' + _list[0]).convert('RGB')
        
        pil_bb, pil_cropped = crop_pil(pil_sample
                                      ,crop_coor = (_coor_ul_w, _coor_ul_h, _coor_dr_w, _coor_dr_h)
                                      ,line_color = _line_color_string
                                      ,line_thickness = _line_thickness
                                      ,line_style_dash = _line_solid_dash
                                      ,line_dash_length = _dash_length
                                      ,line_dash_interval = _dash_interval
                                      )
        
        imshow_pil(pil_bb)
        imshow_pil(pil_cropped)
    except:
        pass


def change_line_color():
    global _line_color_tuple, _line_color_string
    _line_color_tuple, _line_color_string = askcolor(title="Change Line Color")
    tk_1_label_line_color = tki.Label(tk_main, text=_blank, bg=_line_color_string).grid(row=9, column=1)

def change_line_type():
    global _line_solid_dash
    
    tk_1_label_line_type      = tki.Label(tk_main, text=_blank, bg='white').grid(row=10, column=1)
    if _line_solid_dash:
        _line_solid_dash = False
        tk_1_label_line_type      = tki.Label(tk_main, text=_line_solid, bg='white').grid(row=10, column=1)
    else:
        _line_solid_dash = True
        tk_1_label_line_type      = tki.Label(tk_main, text=_line_dash, bg='white').grid(row=10, column=1)

def change_line_option():
    global _line_thickness, _dash_length, _dash_interval
    
    _line_thickness = int(tk_1_entry_line_thickness.get())
    _dash_length    = int(tk_1_entry_dash_length.get())
    _dash_interval  = int(tk_1_entry_dash_interval.get())
    
    _str =  "Line Thickness: " + str(_line_thickness) + "       If Line Type is Dash ( _  _  _ )"
    _str += ", Dash Length: " + str(_dash_length) + "  and  Dash Interval: " + str(_dash_interval)
    tk_1_label_line_info      = tki.Label(tk_main, text=_blank, bg='white').grid(row=11, column=1)
    tk_1_label_line_info      = tki.Label(tk_main, text=_str, bg='white').grid(row=11, column=1)


def crop_them_all():
    global _path, _list, _coor_ul_w, _coor_ul_h, _coor_dr_w, _coor_dr_h
    global _line_color_tuple, _line_color_string, _line_solid_dash, _line_thickness, _dash_length, _dash_interval 
    
    _count = 0
    
    for i_file in _list:
        try:
            in_pil = Image.open(_path + '/' + i_file).convert('RGB')
            pil_bb, pil_cropped = crop_pil(in_pil
                                          ,crop_coor = (_coor_ul_w, _coor_ul_h, _coor_dr_w, _coor_dr_h)
                                          ,line_color = _line_color_string
                                          ,line_thickness = _line_thickness
                                          ,line_style_dash = _line_solid_dash
                                          ,line_dash_length = _dash_length
                                          ,line_dash_interval = _dash_interval
                                          )
        except:
            print("PIL load FAIL:", i_file)
            pil_bb, pil_cropped = None, None
        
        if pil_bb is not None and pil_cropped is not None:
            try:
                if not os.path.exists(_path + '/CROPPED'):
                    os.makedirs(_path + '/CROPPED')
                pil_bb.save(_path + '/CROPPED/_B_' + i_file)
                print("PIL saved!", _path + '/CROPPED/_B_' + i_file)
                pil_cropped.save(_path + '/CROPPED/_C_' + i_file)
                print("PIL saved!", _path + '/CROPPED/_C_' + i_file)
                _count += 1
                
                #tk_1_label_cropping       = tki.Label(tk_main, text=_blank, bg='white').grid(row=18, column=1)
                #tk_1_label_cropping       = tki.Label(tk_main, text="Cropping " + str(_count) + "..." , bg='white').grid(row=18, column=1)
                
            except:
                print("PIL save FAIL:", i_file)
    
    if _count == 0:
        tk_1_label_cropping       = tki.Label(tk_main, text=_blank, bg='white').grid(row=18, column=1)
        tk_1_label_cropping       = tki.Label(tk_main, text="Nothing Happened...", bg='white').grid(row=18, column=1)
    else:
        if _line_solid_dash:
            _str = "Dash ( _ _ _ )"
        else:
            _str = "Solid ( _____ )"
        
        write_txt(_path + "/CROPPED"
                 ,""
                 ,"--- [ Coor Info ] ---"
                 ,"Up Left Width: "     + str(_coor_ul_w)
                 ,"Up Right Height: "   + str(_coor_ul_h)
                 ,"Down Left Width: "   + str(_coor_dr_w)
                 ,"Down Right Height: " + str(_coor_dr_h)
                 ,""
                 ,"--- [ Line Info ] ---"
                 ,"Line Color: (" + str(_line_color_tuple[0]) + ", " + str(_line_color_tuple[1]) + ", " + str(_line_color_tuple[2]) + "), " + str(_line_color_string)
                 ,"Line Type: " + _str
                 ,"Line Thickness: " + str(_line_thickness)
                 ,"Dash Length: " + str(_dash_length)
                 ,"Dash Interval: " + str(_dash_interval)
                 )
        
        tk_1_label_cropping       = tki.Label(tk_main, text=_blank, bg='white').grid(row=18, column=1)
        tk_1_label_cropping       = tki.Label(tk_main, text="Cropped " + str(_count) + " images!" , bg='white').grid(row=18, column=1)




if __name__ == '__main__':
    #print("main")
    
    _path = "     Press [Apply] to update path    "     # working directory
    _list = []                                          # image file name list
    
    _coor_ul_w = 0
    _coor_ul_h = 0
    _coor_dr_w = 0
    _coor_dr_h = 0
    
    _line_color_tuple   = (255, 0, 0)   # Red
    _line_color_string  = '#ff0000'     # Red
    _line_solid_dash    = True          # True: Dash / False: Solid
    _line_thickness     = 5
    _dash_length        = 3
    _dash_interval      = 2
    #-------
    
    tk_main = tki.Tk()
    tk_main.iconbitmap("./resources/icon.ico")
    tk_main.title('Cropper')
    tk_main.geometry("1100x500")
    tk_main.resizable(True, True)
    
    #<<< col: 0
    tk_0_label_entry_path     = tki.Label(tk_main, text=" Enter path ").grid(row=0, column=0)
    tk_0_label_curr_path      = tki.Label(tk_main, text=" Current path ").grid(row=1, column=0)
    
    tk_0_label_void_1         = tki.Label(tk_main, text=" ").grid(row=2, column=0)
    tk_0_label_coor           = tki.Label(tk_main, text=" Crop Coor ").grid(row=3, column=0)
    tk_0_label_up_left_w      = tki.Label(tk_main, text=" Up Left Width ").grid(row=4, column=0)
    tk_0_label_up_left_h      = tki.Label(tk_main, text=" Up Left Height ").grid(row=5, column=0)
    tk_0_label_down_right_w   = tki.Label(tk_main, text=" Down Right Width ").grid(row=6, column=0)
    tk_0_label_down_right_h   = tki.Label(tk_main, text=" Down Right Height ").grid(row=7, column=0)
    
    tk_0_label_void_2         = tki.Label(tk_main, text=" ").grid(row=8, column=0)
    tk_0_label_line_color     = tki.Label(tk_main, text=" Line Color ").grid(row=9, column=0)
    tk_0_label_line_type      = tki.Label(tk_main, text=" Line Type ").grid(row=10, column=0)
    tk_0_label_line_info      = tki.Label(tk_main, text=" Line Info ").grid(row=11, column=0)
    
    tk_0_label_line_thickness = tki.Label(tk_main, text=" Line Thickness ").grid(row=12, column=0)
    tk_0_label_dash_length      = tki.Label(tk_main, text=" Dash Length ").grid(row=13, column=0)
    tk_0_label_dash_interval = tki.Label(tk_main, text=" Dash Interval ").grid(row=14, column=0)
    
    tk_0_label_void_3         = tki.Label(tk_main, text=" ").grid(row=15, column=0)
    tk_0_label_void_4         = tki.Label(tk_main, text=" ").grid(row=16, column=0)
    tk_0_label_void_5         = tki.Label(tk_main, text=" ").grid(row=17, column=0)
    #>>> col: 0
    #<<< col: 1
    tk_1_entry_path = tki.Entry(tk_main, width=120)
    tk_1_entry_path.grid(row=0, column=1)
    tk_1_label_curr_path_info = tki.Label(tk_main, text=" No input yet... ", bg='white').grid(row=1, column=1)
    
    tk_1_label_curr_coor_info    = tki.Label(tk_main, text=" No input yet... ", bg='white').grid(row=3, column=1)
    tk_1_entry_coor_up_left_w    = tki.Entry(tk_main, width=120)
    tk_1_entry_coor_up_left_h    = tki.Entry(tk_main, width=120)
    tk_1_entry_coor_down_right_w = tki.Entry(tk_main, width=120)
    tk_1_entry_coor_down_right_h = tki.Entry(tk_main, width=120)
    tk_1_entry_coor_up_left_w.grid(row=4, column=1)
    tk_1_entry_coor_up_left_h.grid(row=5, column=1)
    tk_1_entry_coor_down_right_w.grid(row=6, column=1)
    tk_1_entry_coor_down_right_h.grid(row=7, column=1)
    tk_1_entry_coor_up_left_w.insert(0, str(_coor_ul_w))
    tk_1_entry_coor_up_left_h.insert(0, str(_coor_ul_h))
    tk_1_entry_coor_down_right_w.insert(0, str(_coor_dr_w))
    tk_1_entry_coor_down_right_h.insert(0, str(_coor_dr_h))
    
    
    
    tk_1_label_line_color     = tki.Label(tk_main, text=_blank, bg=_line_color_string).grid(row=9, column=1)
    tk_1_label_line_type      = tki.Label(tk_main, text=_blank, bg='white').grid(row=10, column=1)
    if _line_solid_dash:
        tk_1_label_line_type  = tki.Label(tk_main, text=_line_dash, bg='white').grid(row=10, column=1)
    else:
        tk_1_label_line_type  = tki.Label(tk_main, text=_line_solid, bg='white').grid(row=10, column=1)
    
    _str =  "Line Thickness: " + str(_line_thickness) + "       If Line Type is Dash ( _  _  _ )"
    _str += ", Dash Length: " + str(_dash_length) + "  and  Dash Interval: " + str(_dash_interval)
    tk_1_label_line_info      = tki.Label(tk_main, text=_blank, bg='white').grid(row=11, column=1)
    tk_1_label_line_info      = tki.Label(tk_main, text=_str, bg='white').grid(row=11, column=1)
    
    tk_1_entry_line_thickness = tki.Entry(tk_main, width=120)
    tk_1_entry_line_thickness.grid(row=12, column=1)
    tk_1_entry_line_thickness.insert(0, str(_line_thickness))
    tk_1_entry_dash_length    = tki.Entry(tk_main, width=120)
    tk_1_entry_dash_length.grid(row=13, column=1)
    tk_1_entry_dash_length.insert(0, str(_dash_length))
    tk_1_entry_dash_interval  = tki.Entry(tk_main, width=120)
    tk_1_entry_dash_interval.grid(row=14, column=1)
    tk_1_entry_dash_interval.insert(0, str(_dash_interval))
    
    tk_1_label_cropping       = tki.Label(tk_main, text=_blank, bg='white').grid(row=18, column=1)
    tk_1_label_cropping       = tki.Label(tk_main, text="Ready...", bg='white').grid(row=18, column=1)
    #>>> col: 1
    #<<< col: 2
    
    tk_2_button_path = tki.Button(tk_main, text=" Apply path ", command= get_main_path).grid(row=0, column=2)
    tk_2_button_show_sample = tki.Button(tk_main, text=" Show sample ", command= show_sample_image).grid(row=1, column=2)
    
    tk_2_button_get_crop_coor = tki.Button(tk_main, text=" Update coor", command= get_crop_coor).grid(row=3, column=2)
    
    
    tk_2_button_change_line_color  = tki.Button(tk_main, text=" Change Line Color ", command= change_line_color).grid(row=9, column=2)
    tk_2_button_change_line_type   = tki.Button(tk_main, text=" Change Line Type ", command= change_line_type).grid(row=10, column=2)
    tk_2_button_change_line_option = tki.Button(tk_main, text=" Change Line Option ", command= change_line_option).grid(row=11, column=2)
    
    
    tk_2_button_show_sample_crop   = tki.Button(tk_main, text=" Show crop sample ", command= show_crop_sample_image).grid(row=16, column=2)
    tk_2_button_crop_them_all      = tki.Button(tk_main, text=" Crop Them All ", command= crop_them_all).grid(row=18, column=2)
    #>>> col: 2
    
    
    
    tk_main.mainloop()
    print("Finished")