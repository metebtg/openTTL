import json
import os
import tkinter as tk
from tkinter import ttk


CONF_DATA_PATH = f'{os.path.expanduser("~")}/.config/opentldata.conf'

class SettingsPage(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)        

        self.frame = ttk.Frame(self)       
        self.frame.pack(side="top", fill="both", expand=True)

        label = ttk.Label(self.frame, relief='raised', borderwidth=4, text='Translators')
        label.pack(pady=10, padx=10)          

        self.engin_type = tk.StringVar()
        self.engin_type.set(self._get_default_engine())
        radio_item = ttk.Radiobutton(
            self.frame,
            text='Google Translator',
            value='google',
            variable=self.engin_type,
            command=self._update_config
        )
        radio_item.pack(fill='x', padx=5, pady=5)

        radio_item1= ttk.Radiobutton(
            self.frame,
            text='Duckduckgo Translator',
            value='duckduckgo',
            variable=self.engin_type,
            command=self._update_config
        )
        radio_item1.pack(fill='x', padx=5, pady=5)

    def _update_config(self):
        data = {}

        try:
            with open(CONF_DATA_PATH, 'r') as file:
                data = json.loads(file.read())  
        except (KeyError, FileNotFoundError):
            pass
        
        data['engine'] = self.engin_type.get()
        with open(CONF_DATA_PATH, 'w') as file:
            file.write(json.dumps(data, indent=2))

        

    def _get_default_engine(self):
        try:
            with open(CONF_DATA_PATH, 'r') as file:
                data = json.loads(file.read())
            return  data['engine']
  
        except (KeyError, FileNotFoundError):
            return 'duckduckgo'

        
          
       