# BME547 Final Project
# Katrina Barth, Minhaj Hussain, and Iakov Rachinsky
# GUI Modules

from tkinter import *  # Brings in higher level tools
from tkinter import ttk  # Themed packages
from tkinter import filedialog
from PIL import ImageTk, Image
from pathlib import Path
import io
import base64
import io
import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from matplotlib.pyplot import imread, imshow, show, subplot, title
from matplotlib.pyplot import get_cmap, hist

# Mock variables for testing
img1_path = "Zoey.jpg"
img2_path = "Zoey.jpg"
r1 = [1, 5, 100, 225]
b1 = [4, 90, 100, 90]
g1 = [7, 30, 200, 175]
r2 = [4, 70, 130, 15]
b2 = [113, 80, 234, 190]
g2 = [3, 80, 230, 17]


def main_window():
    root = Tk()
    root.title("Image Processor")
    root.grid_rowconfigure(9, weight=3)
    # Title message
    welcome_msg = ttk.Label(root, text="Welcome to the image processor!",
                            font=(20))
    welcome_msg.grid(column=0, row=0, columnspan=4, pady=15)

    # Labels, boxes, and buttons for image file selection
    def ask_file():
        file_adrs = filedialog.askopenfilename()
        open_file_box.insert(0, file_adrs)
        return
    open_file_lbl = ttk.Label(root,
                              text="Select image file(s) for processing:")
    open_file_lbl.grid(column=0, row=1, pady=5, padx=10)
    file_adrs = StringVar()
    open_file_box = ttk.Entry(root, textvariable=file_adrs)
    open_file_box.config(width=50)
    open_file_box.grid(column=1, row=1, padx=5, columnspan=2)
    browse_btn = ttk.Button(root, text='Browse', command=ask_file)
    browse_btn.grid(column=3, row=1)
    # Frame and radio buttons to choose image processing method
    proc_frm = ttk.Frame(root, borderwidth=1, relief=GROOVE)
    proc_frm.grid(column=0, row=3, pady=5, ipady=5)
    proc_lbl = ttk.Label(proc_frm, text="Select image processing method")
    proc_lbl.grid(column=0, row=0, pady=5)
    proc_choice = StringVar()
    proc_choice.set('Hist')
    proc_1 = ttk.Radiobutton(proc_frm, text="Histogram Equalization",
                             variable=proc_choice,
                             value='Hist')
    proc_1.grid(column=0, row=1, sticky=W, padx=20)
    proc_2 = ttk.Radiobutton(proc_frm, text="Contrast Stretching",
                             variable=proc_choice,
                             value='Contrast')
    proc_2.grid(column=0, row=2, sticky=W, padx=20)
    proc_3 = ttk.Radiobutton(proc_frm, text="Log Compression",
                             variable=proc_choice,
                             value='Log')
    proc_3.grid(column=0, row=3, sticky=W, padx=20)
    proc_4 = ttk.Radiobutton(proc_frm, text="Reverse Video",
                             variable=proc_choice,
                             value='Reverse')
    proc_4.grid(column=0, row=4, sticky=W, padx=20)

    # Button to send image to server for processing and open up next window
    def img_proc():
        proc = proc_choice.get()
        img_path = open_file_box.get()
        print(img_path)
        print(proc)
        window2("Zoey.jpg", "Zoey.jpg")
    proc_btn = ttk.Button(root, text="Process my image(s)",
                          command=img_proc)
    proc_btn.grid(column=1, row=3, columnspan=3, pady=10)
    root.mainloop()
    return


def window2(img1_file, img2_file):
    window2 = Toplevel()
    window2.title("Processed Image Viewer")
    # Frame and Label for Original Image
    img1_lbl = ttk.Label(window2, text="Original Image",
                         font='Arial 10 bold')
    img1_lbl.grid(column=0, row=0, columnspan=4, pady=5)
    img1_frm = ttk.Frame(window2, borderwidth=1, relief=GROOVE,
                         width=375, height=375)
    img1_frm.grid(column=0, row=1, columnspan=4, rowspan=2, pady=5,
                  padx=5, ipady=5)
    img1_frm.grid_propagate(0)
    img1_obj = Image.open(img1_path)
    size = (375, 375)
    img1_obj.thumbnail(size)
    img1 = ImageTk.PhotoImage(img1_obj)
    img1_space = ttk.Label(img1_frm, image=img1)
    img1_space.grid(column=0, row=0)
    # Frame and Label for Processed Image
    img2_lbl = ttk.Label(window2, text="Processed Image",
                         font='Arial 10 bold')
    img2_lbl.grid(column=4, row=0, pady=5)
    img2_frm = ttk.Frame(window2, borderwidth=1, relief=GROOVE,
                         width=375, height=375)
    img2_frm.grid(column=4, row=1, rowspan=2, pady=5, padx=5, ipady=5)
    img2_frm.grid_propagate(0)
    img2_obj = Image.open(img2_path)
    img2_obj.thumbnail(size)
    img2 = ImageTk.PhotoImage(img2_obj)
    img2_space = ttk.Label(img2_frm, image=img2)
    img2_space.grid(column=0, row=0)
    # Frame for metadata
    data_frm = ttk.Frame(window2, borderwidth=1, relief=GROOVE,
                         width=200, height=95)
    data_frm.grid(column=5, row=1, columnspan=2, pady=5, padx=5, sticky=N)
    data_frm.grid_propagate(0)
    timestamp_lbl = ttk.Label(data_frm, text="Time of Upload:")
    timestamp_lbl.grid(column=0, row=0, pady=5, sticky=W)
    proctime_lbl = ttk.Label(data_frm, text="Time for Processing:")
    proctime_lbl.grid(column=0, row=1, pady=5, sticky=W)
    size_lbl = ttk.Label(data_frm, text="Image Size:")
    size_lbl.grid(column=0, row=2, pady=5, sticky=W)
    # Button to open histogram window
    window2.grid_rowconfigure(2, weight=1)
    histo_btn = ttk.Button(window2,
                           text='Show Color Histograms',
                           command=lambda: plt_histo(img1_path, img2_path))
    histo_btn.grid(column=5, row=2, pady=10, columnspan=2, sticky=N)
    # Choose the save file type, with JPEG as default
    file_type = StringVar()
    file_type_lbl = ttk.Label(window2,
                              text="Select save file type:")
    file_type_lbl.grid(column=0, row=3, sticky=E, pady=5, padx=5)
    jpg_box = ttk.Radiobutton(window2, text='JPEG',
                              variable=file_type, value='.jpg')
    jpg_box.grid(column=1, row=3, padx=15, sticky=W)
    png_box = ttk.Radiobutton(window2, text='PNG',
                              variable=file_type, value='.png')
    png_box.grid(column=2, row=3, padx=15, sticky=W)
    tiff_box = ttk.Radiobutton(window2, text='TIFF',
                               variable=file_type, value='.tiff')
    tiff_box.grid(column=3, row=3, padx=15, sticky=W)
    file_type.set('.jpg')

    # Choosing a save location for the processed image
    def ask_file():
        save_file_adrs = filedialog.askopenfilename()
        save_file_box.insert(0, save_file_adrs)
        window2.lift()
        return save_file_adrs

    # Saving the file
    def save_file():
        img2_obj.save(save_file_adrs)
        pass
    save_file_lbl = ttk.Label(window2, text="Save processed image as:")
    save_file_lbl.grid(column=0, row=4, sticky=E, pady=5, padx=5)
    save_file_adrs = StringVar()
    save_file_box = ttk.Entry(window2, textvariable=save_file_adrs)
    save_file_box.grid(column=1, row=4, columnspan=4, padx=5)
    save_file_box.config(width=105)
    browse_btn = ttk.Button(window2, text='Browse', command=ask_file)
    browse_btn.grid(column=5, row=4, sticky=W)
    save_btn = ttk.Button(window2, text="Save Processed Image",
                          command=save_file)
    save_btn.grid(column=6, row=4, pady=5, padx=5)
    # Close window button
    close_btn = ttk.Button(window2, text="Close Processed Image Viewer",
                           command=window2.destroy)
    close_btn.grid(column=0, row=5, columnspan=7, pady=10)
    window2.mainloop()
    return


def plt_histo(img1_path, img2_path):
    img1 = imread(img1_path)
    img2 = imread(img1_path)
    img1_shape = img1.shape
    img2_shape = img2.shape
    r1 = []
    g1 = []
    b1 = []
    r2 = []
    g2 = []
    b2 = []
    for i in range(img1_shape[0]):
        for j in range(img1_shape[1]):
            r1.append(img1[i, j, 0])
            g1.append(img1[i, j, 1])
            b1.append(img1[i, j, 2])
    for i in range(img2_shape[0]):
        for j in range(img2_shape[1]):
            r2.append(img2[i, j, 0])
            g2.append(img2[i, j, 1])
            b2.append(img2[i, j, 2])
    # Plot Histogram for original image
    plt.figure(1)
    plt.suptitle('Original Image')
    subplot(311)
    hist(r1, 256, range=(0, 256), color='red')
    title('Red')
    subplot(312)
    hist(g1, 256, range=(0, 256), color='green')
    title('Green')
    subplot(313)
    hist(b1, 256, range=(0, 256), color='blue')
    title('Blue')
    plt.tight_layout()
    plt.subplots_adjust(top=0.88, right=0.93)
    plt.subplots_adjust(top=0.88)
    # Histogram for processed image
    plt.figure(2)
    plt.suptitle('Processed Image')
    subplot(311)
    hist(r2, 256, range=(0, 256), color='red')
    title('Red')
    subplot(312)
    hist(g2, 256, range=(0, 256), color='green')
    title('Green')
    subplot(313)
    hist(b2, 256, range=(0, 256), color='blue')
    title('Blue')
    plt.tight_layout()
    plt.subplots_adjust(top=0.88, right=0.93)
    plt.show()
    return


if __name__ == '__main__':
    main_window()