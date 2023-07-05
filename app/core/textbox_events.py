import tkinter as tk

## EVENTS ##
def textbox_select_all(event): 
    textbox = event.widget
    textbox.tag_add(tk.SEL, "1.0", 'end-1c')
    textbox.mark_set(tk.INSERT, "1.0")
    textbox.see(tk.INSERT)
    return 'break' ##Dont works without this line.

def textbox_paste(event):  
    textbox = event.widget
    if textbox.master.clipboard_get():     
        ranges = textbox.tag_ranges(tk.SEL)    
        if ranges:
            textbox.delete('sel.first', 'sel.last')  
        textbox.insert(textbox.index(tk.INSERT), textbox.master.clipboard_get())
    return 'break' ##Dont works without this line.

def textbox_copy(event=None, textbox=None):  
  
    if not textbox:
        textbox = event.widget  

    if textbox and textbox.tag_ranges(tk.SEL):            
        textbox.master.clipboard_clear() 
        textbox.master.clipboard_append(textbox.selection_get())

    elif textbox:
        textbox.master.clipboard_clear() 
        text = textbox.get("1.0","end").strip()
        textbox.master.clipboard_append(text)
        

def textbox_cut(event):
    textbox = event.widget
    if textbox.tag_ranges(tk.SEL):            
        textbox.master.clipboard_clear() 
        textbox.master.clipboard_append(textbox.selection_get())
        textbox.delete('sel.first', 'sel.last')