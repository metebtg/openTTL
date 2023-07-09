import json
import os
import tkinter as tk
from tkinter import ttk
from json.decoder import JSONDecodeError

from . import CONF_DATA_PATH


class SettingsPage(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.frame = ttk.Frame(self)
        self.frame.pack(side="top", fill="both", expand=True)

        label = ttk.Label(self.frame, relief='raised', borderwidth=4, text='Translators')
        label.pack(pady=10, padx=10)

        self.engin_type = tk.StringVar()
        self.engin_type.set(self._get_default_engine())

        radio_data = (('Google Translator', 'google'), ('Duckduckgo Translator', 'duckduckgo'))
        for _ in radio_data:

            radio = ttk.Radiobutton(
                self.frame,
                text=_[0],
                value=_[1],
                variable=self.engin_type,
                command=self._update_config)

            radio.pack(fill='x', padx=5, pady=5)

    def _update_config(self):
        data = {}

        try:
            with open(CONF_DATA_PATH, 'r') as file:
                data = json.load(file)
        except (KeyError, FileNotFoundError, JSONDecodeError) as error:
            print(error)

        data['engine'] = self.engin_type.get()
        with open(CONF_DATA_PATH, 'w') as file:
            json.dump(data, file, indent=2)

    def _get_default_engine(self):
        try:
            with open(CONF_DATA_PATH, 'r') as file:
                data = json.load(file)
            return  data['engine']
        except (KeyError, FileNotFoundError, JSONDecodeError) as error:
            print(error)
            return 'duckduckgo'
