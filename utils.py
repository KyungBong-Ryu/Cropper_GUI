import os
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter, ImageDraw
import cv2
import numpy as np

def load_file_list(in_path):
    #out_list = os.listdir(in_path)
    #print(out_list)
    #return out_list
    return os.listdir(in_path)

#PIL 이미지 출력
def imshow_pil(in_pil, **kargs):
    '''
    imshow_pil(#pil image show with plt function
               in_pil
               #(선택) (tuple) 출력 크기
              ,figsize = (,)
               #(선택) (bool) pil 이미지 정보 출력 여부 (default = True)
              ,print_info = 
              )
    '''
    
    try:
        plt.figure(figsize = kargs['figsize'])
    except:
        pass
    plt.imshow(np.array(in_pil))
    
    try:
        _str = ("Format: " + str(in_pil.format) 
               +"  Mode: " + str(in_pil.mode) 
               +"  Size (w,h): " +  str(in_pil.size[0]) + "," + str(in_pil.size[1]))
        plt.title(_str)
    except:
        pass
    
    plt.show()
    
    '''
    try:
        print_info = kargs['print_info']
    except:
        print_info = True
    
    
    if print_info:
        try:
            print("Format:", in_pil.format, "  Mode:", in_pil.mode, "  Size (w,h):", in_pil.size)
        except:
            print("Format: No Info", "  Mode:", in_pil.mode, "  Size (w,h):", in_pil.size)
    '''
    
    

#=== End of imshow_pil



# pil crop 영역 점선으로 box 표현 & cropeed image 생성

def crop_pil(in_pil, **kargs):
    
    crop_coor = kargs['crop_coor'] # tuple with (UL w, UL h, DR w, DR h)
    
    try:
        line_color = kargs['line_color']
    except:
        line_color = 'red'
    
    try:
        line_thickness = kargs['line_thickness']
    except:
        line_thickness = 5
    
    try:
        line_style_dash = bool(kargs['line_style_dash'])            # (bool) 점선여부
    except:
        line_style_dash = False
    
    if line_style_dash:
        try:
            line_dash_length = int(kargs['line_dash_length'])       # (int) 점선 길이
        except:
            line_dash_length = 2
        
        try:
            line_dash_interval = int(kargs['line_dash_interval'])   # (int) 점선 간격
        except:
            line_dash_interval = line_dash_length
    else:
        line_dash_length = None
        line_dash_interval = None
    
    _ul_w, _ul_h, _dr_w, _dr_h = crop_coor
    
    if _ul_w==_dr_w and _ul_h==_dr_h:
        return None, None
    
    pil_cropped = in_pil.crop(crop_coor)
    
    pil_bb = in_pil.copy()
    
    # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.line
    if line_style_dash:
        
        _list_coor = [((_ul_w, _ul_h), (_dr_w, _ul_h))
                     ,((_dr_w, _ul_h), (_dr_w, _dr_h))
                     ,((_dr_w, _dr_h), (_ul_w, _dr_h))
                     ,((_ul_w, _dr_h), (_ul_w, _ul_h))
                     ]
        
        for _start, _finish in _list_coor:
            print("start", _start, "finish", _finish)
            pil_bb = draw_dash(in_pil = pil_bb
                              ,coor_start = _start
                              ,coor_finish = _finish
                              ,line_color = line_color
                              ,line_thickness = line_thickness
                              ,line_length = line_dash_length
                              ,line_interval = line_dash_interval
                              )
        
    else:
        draw_bb = ImageDraw.Draw(pil_bb)
        draw_bb.line([(_ul_w, _ul_h), (_dr_w, _ul_h), (_dr_w, _dr_h), (_ul_w, _dr_h), (_ul_w, _ul_h)]
                    ,fill  = line_color
                    ,width = line_thickness
                    ,joint = None
                    )
    
    
    
    return pil_bb, pil_cropped
    
#=== End of crop_pil




def draw_dash(**kargs):
    
    in_pil          = kargs['in_pil'].copy()        # (pil) 입력 이미지
    draw_line       = ImageDraw.Draw(in_pil)
    
    coor_start      = kargs['coor_start']           # (tuple) 시작 좌표 (w,h) 
    coor_finish     = kargs['coor_finish']          # (tuple) 종료 좌표 (w,h)
    start_w,  start_h  = int(coor_start[0]),  int(coor_start[1])
    finish_w, finish_h = int(coor_finish[0]), int(coor_finish[1])
    
    line_color      = kargs['line_color']           # (str) 선 색깔
    line_thickness  = int(kargs['line_thickness'])  # (int) 선 두께
    line_length     = int(kargs['line_length'])     # (int) dash 선 길이
    line_interval   = int(kargs['line_interval'])   # (int) dash 간격 길이
    
    
    # direction check (width)
    if start_w < finish_w:      # 오른쪽으로
        go_w = 1
    elif start_w > finish_w:    # 왼쪽으로
        go_w = -1
    else:                       # 정지
        go_w = 0
    
    # direction check (height)
    if start_h < finish_h:      # 아래쪽으로
        go_h = 1
    elif start_h > finish_h:    # 위쪽으로
        go_h = -1
    else:                       # 정지
        go_h = 0
    
    a_w, a_h = start_w, start_h     # dash start coor
    b_w = a_w + line_length*go_w    # dash finish coor
    b_h = a_h + line_length*go_h
    
    #print("outside while loop")
    while (a_w*go_w <= finish_w*go_w) and (a_h*go_h <= finish_h*go_h):
        #print("intside while loop") #현재 loop 진입이 안됨
        if (go_w == 0) and (go_h == 0):
            print("Don't need to draw dash")
            break
        
        # min 함수로 end 최대좌표 제한걸기 -> go_? 음수 고려해서 absolute 사용하기
        # (여기에 기능추가)
        
        if go_w != 0:
            b_w = abs(min(b_w*go_w, finish_w*go_w))
        
        if go_h != 0:
            b_h = abs(min(b_h*go_h, finish_h*go_h))
        
        #print(a_w, a_h, b_w, b_h)
        
        draw_line.line([(a_w, a_h), (b_w, b_h)]
                      ,fill  = line_color
                      ,width = line_thickness
                      ,joint = None
                      )
        
        a_w, a_h = a_w + (line_length+line_interval)*go_w, a_h + (line_length+line_interval)*go_h
        b_w, b_h = b_w + (line_length+line_interval)*go_w, b_h + (line_length+line_interval)*go_h
    
    return in_pil


#[(x+30, y), (x-10, y+h), (x+w-20, y+h+50), (x+w+40, y+47), (x+30, y)],