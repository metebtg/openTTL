import os
import json
from googletrans import Translator
from .translator_duck import TranslatorDuck
import tkinter as tk
from tkinter import Menu, ttk, messagebox
import time
from json.decoder import JSONDecodeError

from .utils import get_engine_data, code_to_lang, lang_to_code, get_index, get_path
from .right_click import show_right_click_menu
from .textbox_events import textbox_select_all, textbox_paste, textbox_copy


BG_COLOR = "#A27B5C"
FG_COLOR = "#DCD7C9"
LANG_DATA_PATH = f'{os.path.expanduser("~")}/.config/opentltranslations.json'
CONF_DATA_PATH = f'{os.path.expanduser("~")}/.config/opentldata.conf'


engine_data = get_engine_data('google')
engine_langs = [_['lang'] for _ in engine_data]


class TranslatePage(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        ## TEXTBOXES ##

        # textbox bindings
        bindings = (
            ("<Button-3>", lambda event: show_right_click_menu(event)),
            ('<Shift-Return>', self.get_translate),
            ('<Control-Return>', self.add_to_db),
            ('<Control-a>', lambda event: textbox_select_all(event)),
            ('<Control-v>', lambda event: textbox_paste(event)),
        )

        textbox_data = (('left', 0), ('right', 3))
        for data in textbox_data:
            self.__dict__[f'{data[0]}_textbox'] = tk.Text(
                self,
                height=8,
                width=25,
                highlightthickness=0,
                background=FG_COLOR,
                wrap=tk.WORD
            )
            textbox = self.__dict__[f'{data[0]}_textbox']
            textbox.grid(column=data[1], row=1, padx=5, pady=5, rowspan=5, sticky='nsew')
            if data[0] == 'left':
                textbox.focus()
            # Set bindings
            for binding in bindings:
                textbox.bind(binding[0], binding[1])


        ## BUTTONS ##
        # WARNING #
        # image_label is required
        # We dont use them but without them images are not visible.
        img_label = ttk.Label(self)
        swap_button_img = tk.PhotoImage(file=f"{get_path()}/icons/swap_icon.png")
        img_label.image = swap_button_img
        swap_button = ttk.Button(
            self,
            image=swap_button_img,
            command=self.swap_langs,
            cursor=f"exchange",)
        swap_button.grid(column=1, row=0, columnspan=2)

        ## Translate, Clear, Add buttons...
        normal_buttons_data = (
            ('Translate', self.get_translate, 1),
            ('Clear', self.clear_textboxes, 2),
            ('Add', self.add_to_db, 3)
        )
        # Loop and grid them.
        for b_data in normal_buttons_data:
            ttk.Button(
                self,
                text=b_data[0],
                command=b_data[1],
                width=8
            ).grid(column=1, row=b_data[2], columnspan=2)

        ## Copy Buttons
        # Load image for button.
        copy_img_label = tk.Label(self)
        copy_button_img = tk.PhotoImage(file=f"{get_path()}/icons/copy_icon.png")
        copy_img_label.image = copy_button_img

        copy_button_data = (('left', 1), ('right', 2))
        for _ in copy_button_data:
            tk.Button(
                self,
                image=copy_button_img,
                highlightthickness=0,
                bg=BG_COLOR,
                activebackground=BG_COLOR,
                border=0,
                font=("arial", 10, "bold"),
                command=lambda direction=_[0]: self.copy_textbox(direction),
            ).grid(column=_[1], row=4)

        ## COMBOBOXES ##
        left_current, right_current = self.get_combo_data()
        combobox_data = (
            ('left', 0, left_current),
            ('right', 3, right_current)
        )
        for _ in combobox_data:
            self.__dict__[f'{_[0]}_combobox'] = ttk.Combobox(self)
            textbox = self.__dict__[f'{_[0]}_combobox']
            textbox['values'] =  engine_langs
            textbox.current(get_index(engine_data, _[2]))
            textbox.grid(column=_[1], row=0, sticky='ew')
            textbox.bind("<<ComboboxSelected>>", self.default_combo_items)


    ## FUCNTIONS
    def add_to_db(self):
        """Add language data to local json file."""
        src_word = self.left_textbox.get("1.0","end").strip().title()
        dest_word = self.right_textbox.get("1.0","end").strip().title()

        if len(src_word) > 0 and len(dest_word) > 0:
            # Get combobox Language and convert them to lang code

            src_lang = lang_to_code(engine_data, self.left_combobox.get().strip())
            dest_lang = lang_to_code(engine_data, self.right_combobox.get().strip())
            new_data = {
                src_lang: {dest_word: {src_word: dest_word}}
            }

            data: dict = {}
            try:
                with open(LANG_DATA_PATH, "r") as file:
                    data = json.load(file)
                if src_lang not in data:
                    data[src_lang] = {}
                if dest_word not in data[src_lang]:
                    data[src_lang][dest_word] = {}

                data[src_lang][dest_word][src_word] = dest_word
            except (KeyError, FileNotFoundError, JSONDecodeError) as error:
                print(error)
                data = new_data
            finally:
                with open(LANG_DATA_PATH, "w") as file:
                    json.dump(data, file, indent=2, ensure_ascii=False)

        # Refresh query page data
        # get study_page
        study_page = self.parent.winfo_children()[1].winfo_children()[0].winfo_children()
        # for frame object in study_page, this is for prevent attribute error
        for object_ in study_page:
            # if page is QueryPage
            if hasattr(object_, 'refresh_data'):
                    object_.refresh_data()
                    break

    def copy_textbox(self, direction):
        print(direction)
        if direction == 'left':
            textbox = self.left_textbox
        else:
            textbox = self.right_textbox

        textbox_copy(event=None, textbox=textbox)

    def swap_langs(self):
        left_combobox = self.left_combobox.get()
        right_combobox = self.right_combobox.get()
        self.left_combobox.current(get_index(engine_data, right_combobox))
        self.right_combobox.current(get_index(engine_data, left_combobox))

        left_textbox = self.left_textbox.get("1.0","end").strip()
        right_textbox = self.right_textbox.get("1.0","end").strip()

        self.left_textbox.delete("1.0", "end")
        self.left_textbox.insert("end", right_textbox)

        self.right_textbox.delete("1.0", "end")
        self.right_textbox.insert("end", left_textbox)

        # Even on swap change langs on conf
        self.default_combo_items()

    def get_translate(self) -> str:
        in_text = self.left_textbox.get("1.0","end").strip()
        if not in_text:
            return 'break'

        engine = 'duckduckgo'
        if os.path.exists(CONF_DATA_PATH):
            with open(CONF_DATA_PATH, 'r') as file:
                data = json.loads(file.read())
                engine = data['engine']

        src_lang = lang_to_code(engine_data, self.left_combobox.get())
        dest_lang = lang_to_code(engine_data, self.right_combobox.get())

        if engine == 'google':
            translator = Translator()
            translated = translator.translate(in_text, src=src_lang, dest=dest_lang)
            translated_text = translated.text

        else:
            duck = TranslatorDuck()
            translated = duck.translate(in_text, src=src_lang, dest=dest_lang)
            translated_text = translated['translated']

        print(translated_text)
        if not translated_text:
            messagebox.showerror("error", translated_text)

        self.right_textbox.delete("1.0", "end")
        self.right_textbox.insert("end", translated_text)

        return 'break'

    def clear_textboxes(self):
        self.left_textbox.delete("1.0", "end")
        self.right_textbox.delete("1.0", "end")

    def default_combo_items(self, *args):
        # If combo item changes, write it in cfg file
        # User don't have to always choice language
        # User will find last chosen langs in combo
        combobox_data = {
                "leftComboLang": self.left_combobox.get(),
                "rightComboLang": self.right_combobox.get(),
        }

        data: dict = {}
        try:
            with open(CONF_DATA_PATH, 'r') as file:
                data = json.load(file)

        except (FileNotFoundError, JSONDecodeError) as error:
            print(error)
            data = combobox_data

        else:
            data.update(combobox_data)

        finally:
            with open(CONF_DATA_PATH, 'w') as file:
                json.dump(data, file, indent=2)

    def get_combo_data(self):
        """Return default value bor comboboxes"""
        try:
            with open(CONF_DATA_PATH, 'r') as file:
                data = json.load(file)
            return [data['leftComboLang'], data['rightComboLang']]
        except (KeyError, FileNotFoundError, JSONDecodeError):
            return ['English', 'Turkish']
