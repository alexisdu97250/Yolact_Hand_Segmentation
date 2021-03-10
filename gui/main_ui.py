# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 15:56:04 2021

@author: basel
"""

from tkinter import *
from tkinter import ttk

class mainWindow(object):
    def setupUi(self, MainWindow):
        #Define the buttons in the window
        window = Tk()
        
        label = Label(window, text="DWYH_Segmentation")
        label.pack()
        
        
        liste=ttk.Combobox(window, values = ["Image File", "Video File", "Webcam"])
        Label(liste, text = "Input")
        liste.pack(side=LEFT)
        
        Frame1 = Frame(window, borderwidth=2, relief=GROOVE)
        Frame1.pack(side=LEFT, padx=10, pady=10)
        Label(Frame1, text="Source").pack(padx=10, pady=10)
        
        Frame2 = Frame(window, borderwidth=2, relief=GROOVE)
        Frame2.pack(side=RIGHT, padx=10, pady=10)
        Label(Frame2, text="Segmentation Mask").pack(padx=10, pady=10)
        
        button = Button(window, text="Close", command=window.quit)
        button.pack(side = RIGHT)
        window.mainloop() #Display the window