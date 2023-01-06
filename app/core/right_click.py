from tkinter import Menu

from .textbox_events import *


BG_COLOR = "#A27B5C"
FG_COLOR = "#DCD7C9"


class RightClick:
    def __init__(self, event): 
         
        parent = event.widget

        menu = Menu(parent, tearoff=0, background=FG_COLOR)  
        menu.add_command(
            label ="Cut", 
            accelerator="Ctrl+X",
            command=lambda: textbox_cut(event=False, textbox=parent),)  
        menu.add_command(
            label ="Copy", 
            accelerator="Ctrl+C",
            command=lambda: textbox_copy(event=False, textbox=parent),)
        menu.add_command(
            label ="Paste", 
            accelerator="Ctrl+V",
            command=lambda: textbox_paste(event=False, textbox=parent),)        
        menu.add_command(
            label ="Select All", 
            accelerator="Ctrl+A",
            command=lambda: textbox_select_all(event=False, textbox=parent),)
        menu.add_separator()
        menu.add_command(
            label ="Exit", 
            accelerator="Ctrl+Q",
            command=lambda: parent.quit(),)   

        menu.tk_popup(event.x_root, event.y_root)