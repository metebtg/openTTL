import tkinter as tk

## EVENTS ##
def textbox_select_all(event, textbox):    
    textbox.tag_add(tk.SEL, "1.0", 'end-1c')
    textbox.mark_set(tk.INSERT, "1.0")
    textbox.see(tk.INSERT)
    return 'break' ##Dont works without this line.

def textbox_paste(event, textbox):  
    if textbox.master.clipboard_get():     
        ranges = textbox.tag_ranges(tk.SEL)    
        if ranges:
            textbox.delete('sel.first', 'sel.last')  
        textbox.insert(textbox.index(tk.INSERT), textbox.master.clipboard_get())
    return 'break' ##Dont works without this line.

def textbox_copy(event, textbox):    
    if textbox.tag_ranges(tk.SEL):            
        textbox.master.clipboard_clear() 
        textbox.master.clipboard_append(textbox.selection_get())

def textbox_cut(event, textbox):
    if textbox.tag_ranges(tk.SEL):            
        textbox.master.clipboard_clear() 
        textbox.master.clipboard_append(textbox.selection_get())
        textbox.delete('sel.first', 'sel.last')