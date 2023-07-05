from tkinter import Menu

from .textbox_events import *

FG_COLOR = "#DCD7C9"

def show_right_click_menu(event):
    """Show right click menu at event source."""
         
    parent = event.widget
    menu = Menu(parent, tearoff=0, background=FG_COLOR)  
   
    command_data = (
        ("Cut", "Ctrl+X", lambda: textbox_cut(event)),
        ("Copy", "Ctrl+C", lambda: textbox_copy(event)),
        ("Paste", "Ctrl+V", lambda: textbox_paste(event)),
        ("Select All", "Ctrl+A", lambda: textbox_select_all(event)),
        ('seperator'),
        ('Exit', 'Ctrl+Q', lambda: parent.quit())
    )  

    for _ in command_data:
        # if its for add_command
        if len(_) == 3:
            menu.add_command(
                label =_[0], 
                accelerator=_[1],
                command=_[2]
            )
        else:
            menu.add_separator()

    menu.tk_popup(event.x_root, event.y_root)