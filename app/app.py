import tkinter as tk
from tkinter import ttk
import os

from core.translate_page import TranslatePage
# from settings_page import SettingsPage
from core.study_page import StudyPage
from core.utils import get_path


BG_COLOR = "#A27B5C"
FG_COLOR = "#DCD7C9"


class OpenTl(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)  
        
        # Styling
        style = ttk.Style()
        style.configure('TLabel', background=FG_COLOR)
        style.configure('TButton', background=FG_COLOR)        
        style.configure('TFrame', background=BG_COLOR) 
        style.configure('Treeview', background=FG_COLOR, fieldbackground=FG_COLOR) 
        style.configure('TNotebook', background=FG_COLOR, bordercolor=BG_COLOR) 
        style.configure('TNotebook.Tab', background=FG_COLOR) 
        style.map("TNotebook.Tab", background=[("selected", BG_COLOR)])
        style.configure(
            'TCombobox', 
            background=FG_COLOR, 
            arrowcolor=BG_COLOR, 
            fieldbackground=FG_COLOR,
            selectbackground=FG_COLOR)
        self.option_add("*TCombobox*Listbox*Background", FG_COLOR)
        style.configure("Treeview.Heading", background=BG_COLOR, foreground=FG_COLOR)

        # Main container
        container = tk.Frame(self)
        container.pack(side='left', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)        

        tabControl = ttk.Notebook(container)             
        tabControl.add(TranslatePage(tabControl), text='Translate')    
        tabControl.add(StudyPage(tabControl), text='Dictionary')
        # tabControl.add(SettingsPage(tabControl), text ='Settings')     
        tabControl.pack(expand=1, fill ="both")    

        
if __name__ == '__main__':
    app = OpenTl(className='openTTL')    
    app.title("openTTL")
    app.iconphoto(False, tk.PhotoImage(file=f"{get_path()}/icons/app_icon.png"))
    app.resizable(0, 0)
    app.wm_title("openTTL")   
    app.mainloop()