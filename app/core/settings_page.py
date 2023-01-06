import tkinter as tk
from tkinter import ttk


class SettingsPage(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text='Settings Page')
        label.pack(pady=10, padx=10)