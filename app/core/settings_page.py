import tkinter as tk
from tkinter import ttk


class SettingsPage(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)        

        self.frame = ttk.Frame(self)       
        self.frame.pack(side="top", fill="both", expand=True)

        label = ttk.Label(self.frame, text='Settings Page')
        label.pack(pady=10, padx=10)
        r = ttk.Radiobutton(
        self.frame,
        text='hello',
        value='hello',
        variable='xl'
        )
        r.pack(fill='x', padx=5, pady=5)
          
       