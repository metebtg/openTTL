import os 
import json
from googletrans import Translator
import tkinter as tk
from tkinter import Menu, ttk

from .right_click import RightClick
from .utils import *
from .textbox_events import textbox_select_all, textbox_paste


BG_COLOR = "#A27B5C"
FG_COLOR = "#DCD7C9"
LANG_DATA_PATH = f'{os.path.expanduser("~")}/.config/opentltranslations.json'
CONF_DATA_PATH = f'{os.path.expanduser("~")}/.config/opentldata.conf'


class TranslatePage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent) 

        self.parent = parent
        
        ## TEXTBOXES ##
        # Left        
        self.left_textbox = tk.Text(
            self,
            height=8, 
            width=25,
            highlightthickness=0,
            background=FG_COLOR,
            wrap=tk.WORD,)
        self.left_textbox.grid(column=0, row=1, padx=5, pady=5, rowspan=5, sticky='nsew')
        self.left_textbox.bind("<Button-3>", lambda event: RightClick(event))
        self.left_textbox.focus()
        # Bindings
        self.left_textbox.bind(
            '<Control-v>', 
            lambda event: textbox_paste(event=event, textbox=self.left_textbox))        
        self.left_textbox.bind(
            '<Control-a>', 
            lambda event: textbox_select_all(event=event, textbox=self.left_textbox))
        self.left_textbox.bind('<Shift-Return>', lambda event: self.get_translate(self.left_textbox))
        self.left_textbox.bind('<Control-Return>', lambda event: self.add_to_db())

        # Right
        self.right_textbox = tk.Text(
            self,
            height=8, 
            width=25,
            highlightthickness=0,
            background=FG_COLOR,
            wrap=tk.WORD,)
        self.right_textbox.grid(column=3, row=1, padx=5, pady=5, rowspan=5, sticky='nsew')
        # Bindings
        self.right_textbox.bind("<Button-3>", lambda event: RightClick(event))        
        self.right_textbox.bind(
            '<Control-v>', lambda event: textbox_paste(event=event, textbox=self.right_textbox))        
        self.right_textbox.bind('<Control-a>', 
            lambda event: textbox_select_all(event=event, textbox=self.right_textbox))
        self.right_textbox.bind('<Shift-Return>', lambda event: self.get_translate())
        self.right_textbox.bind('<Control-Return>', lambda event: self.add_to_db())

        ## BUTTONS ##        
        swap_button_img = tk.PhotoImage(file=f"{get_path()}/icons/swap_icon.png")
        # Bellow two line is deadly required
        img_label = ttk.Label(self)
        img_label.image = swap_button_img 
        swap_button = ttk.Button(
            self,
            image=swap_button_img,
            command=self.swap_langs,
            cursor=f"exchange",)
        swap_button.grid(column=1, row=0, columnspan=2)

        translate_button = ttk.Button(
            self,
            text="Translate",
            command=self.get_translate,
            width=8,)
        translate_button.grid(column=1, row=1, columnspan=2)

        clear_button = ttk.Button(
            self,
            width=8,
            command=self.clear_textboxes,
            text="Clear",)
        clear_button.grid(column=1, row=2, columnspan=2)

        add_button = ttk.Button(
            self,
            text="Add",
            command=self.add_to_db,
            width=8,)
        add_button.grid(column=1, row=3, columnspan=2)

        ## COMBOBOXES
        self.left_combobox = ttk.Combobox(self)
        self.left_combobox["values"] =  google_list()
        # Default to English.
        self.left_combobox.current(google_list().index(self.get_combo_data()[0]))  
        self.left_combobox.grid(column=0, row=0, sticky='ew')   
        self.left_combobox.bind("<<ComboboxSelected>>", lambda event: self.default_combo_items())   

        self.right_combobox = ttk.Combobox(self)
        self.right_combobox["values"] =  google_list()
        # Default to Turkish.
        self.right_combobox.current(google_list().index(self.get_combo_data()[1]))
        self.right_combobox.grid(column=3, row=0, sticky='ew')
        self.right_combobox.bind("<<ComboboxSelected>>", lambda event: self.default_combo_items())   

    ## FUCNTIONS
    def add_to_db(self):
        """Add language data to local json file."""        
        left = self.left_textbox.get("1.0","end").strip().title()
        right = self.right_textbox.get("1.0","end").strip().title()
        
        if len(left) > 0 and len(right) > 0:     
            # Get combobox Language and with google_value convert them to lang code
            left_lang = google_value(self.left_combobox.get().strip())
            right_lang = google_value(self.right_combobox.get().strip())
            # Schema for new data
            new_data = {
                left_lang: {right_lang: {left: right}}
            }
            # If exist update data, otherwise create...
            if os.path.exists(LANG_DATA_PATH):
                with open(LANG_DATA_PATH, "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
                    # Updating old data with new data
                    
                    if left_lang not in data:
                        data[left_lang] = {}
                    if right_lang not in data[left_lang]:
                        data[left_lang][right_lang] = {}

                    data[left_lang][right_lang][left] = right
                    data.update()
            else:
                data = new_data
                open(LANG_DATA_PATH, "w")  
                
            with open(LANG_DATA_PATH, "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4, ensure_ascii=False)  

        # Refresh query page data
        # get study_page
        study_page = self.parent.winfo_children()[1].winfo_children()[0].winfo_children()
        # for frame object in study_page, this is for prevent attribute error
        for object_ in study_page:
            # if page is QueryPage
            if hasattr(object_, 'refresh_data'):                    
                    object_.refresh_data()
                    break
    
    def swap_langs(self):
        left_combobox = self.left_combobox.get()
        right_combobox = self.right_combobox.get()
        
        self.left_combobox.current(google_list().index(right_combobox))  
        self.right_combobox.current(google_list().index(left_combobox))

        left_textbox = self.left_textbox.get("1.0","end").strip()
        right_textbox = self.right_textbox.get("1.0","end").strip()
        
        self.left_textbox.delete("1.0", "end")
        self.left_textbox.insert("end", right_textbox)               

        self.right_textbox.delete("1.0", "end")
        self.right_textbox.insert("end", left_textbox)

        # Even on swap change langs on conf
        self.default_combo_items()

    def get_translate(self): 
        in_text = self.left_textbox.get("1.0","end").strip()     
        
        if len(in_text) > 0:
            translator = Translator()
            translated_text = translator.translate(
                in_text, 
                src=google_value(self.left_combobox.get()), 
                dest=self.right_combobox.get()).text
            
            self.right_textbox.delete("1.0", "end")
            self.right_textbox.insert("end", translated_text)
        
        return 'break' 

    def clear_textboxes(self):
        self.left_textbox.delete("1.0", "end")
        self.right_textbox.delete("1.0", "end")

    def default_combo_items(self):  
        # If combo item changes, write it in cfg file
        # User don't have to always choice language
        # User will find last chosen langs in combo      
        
        if not os.path.exists(CONF_DATA_PATH):
            with open(CONF_DATA_PATH, 'w') as file:
                data = {
                    "leftComboLang": self.left_combobox.get(),
                    "rightComboLang": self.right_combobox.get(),
                }
                json.dump(data, file)
        else:
            with open(CONF_DATA_PATH, 'r') as file:
                data = json.load(file)
            
            data['leftComboLang'] = self.left_combobox.get()
            data['rightComboLang'] = self.right_combobox.get()            

            with open(CONF_DATA_PATH, 'w') as file:
                json.dump(data, file)
    
    def get_combo_data(self):
        # If user ever choice any language in comboboxes return that,    
        
        if os.path.exists(CONF_DATA_PATH):
            with open(CONF_DATA_PATH, 'r') as file:
                data = json.load(file)
            return [data['leftComboLang'], data['rightComboLang']]
        else:
            return ['English', 'Turkish']