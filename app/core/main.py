import tkinter as tk
from tkinter import ttk

from .translate_page import TranslatePage
from .settings_page import SettingsPage
from .study_page import StudyPage
from . import BG_COLOR, FG_COLOR


class OpenTl(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        ## Styling
        style = ttk.Style()
        # Put styles in a tuple
        styles = (
            ('TLabel', {'background': FG_COLOR}),
            ('TButton', {'background': FG_COLOR}),
            ('TFrame', {'background': BG_COLOR}),
            ('TLabel', {'background': FG_COLOR}),
            ('Treeview', {'background': FG_COLOR, 'fieldbackground': FG_COLOR}),
            ('TNotebook', {'background': FG_COLOR, 'bordercolor': BG_COLOR}),
            ('TNotebook.Tab', {'background': FG_COLOR}),
        )
        # Loop styles ...
        for _ in styles:
            widget = _[0]
            params = _[1]
            style.configure(widget, **params)

        style.map("TNotebook.Tab", background=[("selected", BG_COLOR)])

        style.configure(
            'TCombobox',
            background=FG_COLOR,
            arrowcolor=BG_COLOR,
            fieldbackground=FG_COLOR,
            selectbackground=FG_COLOR,
            selectforeground='black',
            focusfill='red',
            insertcolor='black')
        style.configure(
            'TRadiobutton',
            background=BG_COLOR,
            foreground='black',
            pressed=BG_COLOR,
            indicatorcolor=BG_COLOR)

        self.option_add("*TCombobox*Listbox*Background", FG_COLOR)
        self.option_add("*TCombobox*Listbox*foreground", 'black')
        self.option_add("*TCombobox*Listbox*selectBackground", '#5089a7')
        self.option_add("*TCombobox*Listbox*selectForeground", 'black')

        style.configure("Treeview.Heading", background=BG_COLOR, foreground=FG_COLOR)

        # Main container
        container = tk.Frame(self)
        container.pack(side='left', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        tab_control = ttk.Notebook(container)
        tab_control.add(TranslatePage(tab_control), text='Translate')
        tab_control.add(StudyPage(tab_control), text='Dictionary')
        tab_control.add(SettingsPage(tab_control), text ='Settings')
        tab_control.pack(expand=1, fill ="both")
