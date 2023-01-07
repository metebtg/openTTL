from core import main, utils
from tkinter import PhotoImage

if __name__ == '__main__':
    app = main.OpenTl(className='openTTL')    
    app.title("openTTL")
    app.iconphoto(False, PhotoImage(file=f"{utils.get_path()}/icons/app_icon.png"))
    app.resizable(0, 0)
    app.wm_title("openTTL")   
    app.mainloop()