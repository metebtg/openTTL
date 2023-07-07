import json
from json.decoder import JSONDecodeError
import tkinter as tk
from tkinter import ttk
import os

from .utils import code_to_lang, google_value, get_engine_data, lang_to_code


BG_COLOR = "#A27B5C"
FG_COLOR = "#DCD7C9"
LANG_DATA_PATH = f'{os.path.expanduser("~")}/.config/opentltranslations.json'

engine_data = get_engine_data('google')
engine_langs = [_['lang'] for _ in engine_data]


class StudyPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent) 

        self.container = ttk.Frame(self)         
        self.container.pack(side="top", fill="both", expand=True)  
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)   

        # Render query page
        self.frames = {} 
        self.frames[QueryPage] = QueryPage(self.container, self)  
        self.frames[QueryPage].grid(row=0, column=0, sticky="nsew")         
        self.show_query_page()
  
    def show_query_page(self):
        self.frames[QueryPage].refresh_data()         
        self.frames[QueryPage].tkraise()        

    def show_result_page(self, combo_data): 
        self.frames[ResultsPage] = ResultsPage(self.container, self, combo_data)  
        self.frames[ResultsPage].grid(row=0, column=0, sticky="nsew")       
        self.frames[ResultsPage].tkraise()  
        

class QueryPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        self.controller = controller        
        # Get data for combo list
        self.items = self.get_data()[0]
        self.data = self.get_data()[1]
        # Label  
        label = ttk.Label(self, relief='raised', borderwidth=4, text='Choose a language')
        label.pack(pady=10, padx=10)        
        # Combobox
        self.combo = ttk.Combobox(self) 
        self.combo['values'] = self.items
        if self.items:
            self.combo.current(0)
        else:
            self.combo['state'] = 'disabled'
        self.combo.pack(pady=10, padx=10)
        # Button
        self.button = ttk.Button(
            self, 
            text='Get', 
            width=7,
            command=self.get_results,)
        self.button.pack(pady=10, padx=10)
        if not self.items:
            self.button['state'] = 'disabled'

    def refresh_data(self):        
        self.items = self.get_data()[0]
        self.data = self.get_data()[1]
        
        if self.items:            
            self.combo['values'] = self.items
            self.combo.current(0)
            self.button['state'] = 'normal'
            self.combo['state'] = 'normal'
        else:
            self.combo['values'] = ['']
            self.combo.current(0)            
            self.button['state'] = 'disabled'

    def get_data(self):
        # Get fresh data in opening        
        data: dict = {}
        try:
            with open(LANG_DATA_PATH) as file:
                data = json.load(file)
        except (KeyError, FileNotFoundError, JSONDecodeError):
            return ['', '']

        items = []
        for key in data:
            for sub_key in data[key]:
                if data[key][sub_key].keys():
                    
                    items.append(
                        f'{code_to_lang(engine_data, key)} --> {code_to_lang(engine_data, sub_key)}'
                    )         
        
        return [items, data]

    # Close our page and get result page with passing data
    def get_results(self):
        combose = self.combo.get().split('-->')
        k_lang = lang_to_code(engine_data, combose[0].strip())
        v_lang = lang_to_code(engine_data, combose[1].strip())
        combo_data = {
            'k_lang': k_lang,
            'v_lang': v_lang,
            'k_list': list(self.data[k_lang][v_lang].keys()),
            'v_list': list(self.data[k_lang][v_lang].values()),
        }          
        self.controller.show_result_page(combo_data)


class ResultsPage(ttk.Frame):
    def __init__(self, parent, controller, combo_data):
        ttk.Frame.__init__(self, parent)
        
        self.combo_data = combo_data
        # Frame for tree and scroll
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, rowspan=20)
        # Scroll
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.grid(row=0, column=1, sticky='ns')        
        # Tree
        self.tree = ttk.Treeview(
            frame,
            columns=(combo_data['k_lang'], combo_data['v_lang']), 
            show='headings',
            height=8, 
            yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)      
        # Tree head data
        self.tree.heading(combo_data['k_lang'], text=code_to_lang(engine_data, combo_data['k_lang']))
        self.tree.heading(combo_data['v_lang'], text=code_to_lang(engine_data, combo_data['v_lang']))
        self.tree.grid(row=0, column=0)

        # With loop insert data to tree
        for (x, y) in zip(combo_data['k_list'], combo_data['v_list']):
            self.tree.insert('', tk.END, values=(x, y))

        # Buttons
        button_back = ttk.Button(
            self, 
            text='Back', 
            width=7,
            command=lambda: controller.show_query_page())
        button_back.grid(row=0, column=1, padx=7, pady=5, sticky='n')
        
        button_del = ttk.Button(
            self, 
            text='Del', 
            width=7,
            command=self.del_word,)
        button_del.grid(row=1, column=1, padx=7, sticky='n')

    def del_word(self):
        """Deletes tree selected item at database and treeview."""
        # If there is selection, otherwise it will errors
        if self.tree.selection():
            to_del = self.tree.item(self.tree.selection()[0])['values'][0]
            # read old data 
            with open(LANG_DATA_PATH, 'r') as file:
                dict_data = json.load(file)
            # Remove unwanted data and write 
            with open(LANG_DATA_PATH, 'w') as file:  
                del dict_data[self.combo_data['k_lang']][self.combo_data['v_lang']][to_del]              
                json.dump(dict_data, file, indent=2)
            # Delete word in also treeview
            self.tree.delete(self.tree.selection()[0])