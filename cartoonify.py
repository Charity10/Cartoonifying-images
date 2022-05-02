from ctypes import resize
from email import message
import numpy as np
import matplotlib.pyplot as plt
import cv2
import easygui
import imageio
import os
import tkinter as tk
import sys
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image


#making the main window
top = tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image')
top.configure(background= 'white')
label = Label(top,background ='#CDCDCD', font = ('calibri', 20, 'bold'))


def location():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)

def cartoonify(ImagePath):
    original_image = cv2.imread(ImagePath)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    #print(original_image)

    if original_image is None:
        print("couldnt find any image, please upload an image")
        sys.exit()

    Resized = cv2.resize(original_image, (3456, 4783))
    #plt.imshow(Resized, cmap= 'gray') 

    grayscaleImage = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    Resized1 = cv2.resize(grayscaleImage, (3456, 4783))

    smoothgrayImage = cv2.medianBlur(grayscaleImage, 1)
    Resized2 = cv2.resize(smoothgrayImage, (3456, 4783))

    getedge = cv2.adaptiveThreshold(smoothgrayImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    Resized3 = cv2.resize(getedge, (3456, 4783))
    

    colorImage = cv2.bilateralFilter(original_image, 9, 200, 200)
    Resized5 = cv2.resize(colorImage, (3456, 4783))

    # colorImage2 = cv2.bilateralFilter(colorImage, 9, 100,50)
    # Resized5 = cv2.resize(colorImage2, (3456, 4783))

    catoonImage = cv2.bitwise_and(colorImage, colorImage, mask = getedge)
    Resized6 = cv2.resize(catoonImage, (3456, 4783))

    images = [Resized, Resized1, Resized2, Resized3, Resized5, Resized6]
    fig, axes = plt.subplots(3,2, figsize = (8,8), subplot_kw ={'xticks': [], 'yticks': []}, gridspec_kw=dict(hspace = 0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap = 'gray')

    save1 = Button(top,text="save cartoon image", command = lambda: save(Resized6, ImagePath), padx=30, pady = 5)
    save1.configure(background = '#364156', foreground = 'white', font =('calibri', 10, 'bold'))
    save1.pack(side = TOP, pady = 50)
    
    plt.show()


def save(Resized6, ImagePath):
    newName = "cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(Resized6, cv2.COLOR_RGB2BGR))
    I = 'image saved by name' + newName + 'at' +path
    tk.messagebox.showinfo(title = None, message = I)


#making the cartooning button in the main window
location = Button(top, text= "cartoonify your Image", command = location, padx = 10, pady =5)
location.configure(background = '#364156', foreground='white', font=('calibri', 10, 'bold'))
location.pack(side=TOP, pady = 50)

top.mainloop()


    
