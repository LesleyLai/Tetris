"""
Provides an interface to a wrapped Tcl/Tk GUI library.
"""
        
import tkinter as tk

class TetrisButtom(tk.Button):
    """
    A convenient wrapper of the Tk's Button class
    """
    
    def __init__(self, parent, text, bg, callback = None):
        "Constructor of the buttom"
        super().__init__(parent, text=text, bg=bg, command=callback)
        
        
