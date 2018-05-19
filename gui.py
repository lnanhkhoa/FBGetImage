#!/usr/bin/python3
# Su dung thu vien Tkinter de lap trinh GUI.
from tkinter import Tk, TOP, BOTH, X, LEFT, RIGHT, BOTTOM, Menu
from tkinter.filedialog import Open 
from tkinter import Frame, Label, Button, Entry#, Style
from tkinter.ttk import Style 
from PIL import Image
from PIL import ImageTk
import tkinter.messagebox as mbox
from tkinter.colorchooser import askcolor
import tkinter as tk
import os
from myQueue import *
from queue import Queue
from threading import Thread

# Khoi tao class cho cua so chinh.

class Example(Frame):
 def __init__(self, parent):
  Frame.__init__(self, parent)
  self.parent = parent
  self.initUI()
# Tao tieu de cho tool.

  
 def initUI(self):
  self.parent.title("Facebook searching tool")
  self.style = Style()
  self.style.theme_use("classic")
 

# Viet loi chao cho tool bang label.

 
  self.pack(fill=BOTH, expand=1)
  frame1 = Frame(self)
  frame1.pack(fill=X)
  lbl1 = Label(frame1, text="         Hello, Welcome to facebook searching tool !!!", font="VNI-Dom 15", width=50, foreground="blue")
  lbl1.pack(side=TOP, padx=8, pady=8, expand=True) 


# Tao menu "Option" cho tool. 


  menubar = Menu(self.parent)
  self.parent.config(menu=menubar)
  fileMenu = Menu(menubar)       
  submenu = Menu(fileMenu)
  submenu.add_command(label="Watching images Button", command=self.onChoose2)
  submenu.add_command(label="Stop Button", command=self.onChoose3)
  submenu.add_command(label="Start Button", command=self.onChoose5)
  submenu.add_command(label="Quit Button", command=self.onChoose1)
  submenu.add_command(label="Background", command=self.onChoose6)
  fileMenu.add_cascade(label='Change colour', menu=submenu)
  fileMenu.add_separator()
  fileMenu.add_command(label="Go to the result folder", command=self.onOpen)
  fileMenu.add_separator()
  fileMenu.add_command(label="Exit", command=self.quit)
  menubar.add_cascade(label="Option", menu=fileMenu)        


# Tao entry de nhap doan text can tim kiem. 


  frame1 = Frame(self)
  frame1.pack(fill=X)
  lbl1 = Label(frame1, text="Key word",font="VNI-Dom 12", foreground="black", width=16)
  lbl1.pack(side=LEFT, padx=18, pady=12)
  self.entry1 = Entry(frame1)
  self.entry1.pack(fill=X, padx=5, expand=True)


# Tao hinh nen giao dien cho tool dung trang tri cho giao dien.


  bard = Image.open("./background.jpg")
  bardejov = ImageTk.PhotoImage(bard)
  label1 = Label(self, image=bardejov)
  label1.image = bardejov
  label1.pack(side=BOTTOM, padx=10, expand=True)


# Tao cac Button cho tool.


  self.quitButton = Button(self, text="Quit", command=self.onQuest, background="black", foreground="white")
  self.quitButton.pack(side=RIGHT, padx=5, pady=5)
  self.okButton1 = Button(self, text="Watching images", command=self.onshowImages, background="black", foreground="white")
  self.okButton1.pack(side=RIGHT, padx=5, pady=5)  
  self.closeButton = Button(self, text="Stop", command=self.onStop, background="black", foreground="white")
  self.closeButton.pack(side=RIGHT, padx=5, pady=5)
  self.okButton = Button(self, text="Start", command=self.onStartentry, background="black", foreground="white")
  self.okButton.pack(side=RIGHT, padx=5, pady=5)
  self.newkeywordButton = Button(self, text="New key word", command=self.onDeleteentry, background="black", foreground="white")
  self.newkeywordButton.pack(side=RIGHT, padx=5, pady=5)


# Viet cac ham con cho Button. 


# Tao nut quit de thoat chuong trinh.

 def onQuest(self):
   outButton = mbox.askquestion("Question", "Are you sure to quit ?")
   if outButton == "yes":
     for i in range(1,10): 
       self.quit()

# Tao command cho nut Stop. 

 def onStop(self):
   stopButton = mbox.askquestion("Question", "Do you want to stop ?")

# Tao command de mo file cho option.

 def onOpen(self):
   ftypes = [('All files', '*'), ('Text files', '*.txt'), ('jpg file', '*.jpg'), ('gif file', '*.gif')]
   dlg = Open(self, filetypes = ftypes)
   fl = dlg.show()
   if fl != '':
    images = fl
    if images.endswith("png") or images.endswith("jpg") or images.endswith("jpeg") or images.endswith("gif") or images.endswith("tiff") or images.endswith("bmp") or images.endswith("PNG") or images.endswith("JPG") or images.endswith("JPEG") or images.endswith("GIF") or images.endswith("TIFF") or images.endswith("BMP"):
     window=tk.Toplevel()
     str = fl.split('/', 100)
     number_last = len(fl.split('/', 100)) - 1
     window.title(str[number_last])
     self.mg = Image.open(fl)
     w, h = Image.open(fl).size
     window.geometry(("%dx%d+300+300") % (w, h))
     window.configure(background='grey')
     path= fl 
     self.img = Image.open(path)
     img = ImageTk.PhotoImage(Image.open(path))
     panel = tk.Label(window, image = img)
     panel.pack(side="bottom", fill="both", expand=True)
     window.mainloop()
    else:
     mbox.showerror("Error", "Could not open file")

# Dinh nghia hop thoai chon mau cho menu option.

 def onChoose1(self):
    (rgb, hx) = askcolor()
    self.quitButton.config(bg=hx)
 def onChoose2(self):
    (rgb, hx) = askcolor()
    self.okButton1.config(bg=hx)
 def onChoose3(self):
    (rgb, hx) = askcolor()
    self.closeButton.config(bg=hx)
 def onChoose4(self):
    (rgb, hx) = askcolor()
    self.okButton.config(bg=hx)
 def onChoose5(self):
    (rgb, hx) = askcolor()
    self.newkeywordButton.config(bg=hx)
 def onChoose6(self):
    (rgb, hx) = askcolor()
    self.config(bg=hx)


# Dinh nghia command cho nut Start Chung ta se lam viec o day.

 def onStartentry(self):
    key_word=self.entry1.get()
    q = Queue(maxsize=0)
    num_threads = 2
    for i in range(num_threads):
        worker = Thread(target=do_stuff, args=(q,))
        worker.setDaemon(True)
        worker.start()
    for x in range(10):
        q.put(x)
    q.join()
    # thread.start()
   # Add code cho nay nhen KhoaL va Phu. Tham so key_word la tu khoa can tim kiem. 

# Dinh nghia command cho nut "New key word".

 def onDeleteentry(self):
   self.entry1.delete(0, 10000)

# Dinh nghia command cho nut "Watching result". 

 def onshowImages(self):
   root = tk.Toplevel() 
   MyApp = ImageClassifyer(root)
   tk.mainloop()

 def edit_config_file(self, text_search):
     pass



# Define cho class cho nut "Watching result".

class ImageClassifyer(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.root.wm_title("Classify Image")   
        src = "./TestImages/"
        self.list_images = []
        for d in os.listdir(src):
          images = d
          if images.endswith("png") or images.endswith("jpg") or images.endswith("jpeg") or images.endswith("gif") or images.endswith("tiff") or images.endswith("bmp") or images.endswith("PNG") or images.endswith("JPG") or images.endswith("JPEG") or images.endswith("GIF") or images.endswith("TIFF") or images.endswith("BMP"): 
            self.list_images.append(d)
        self.frame1 = tk.Frame(self.root, width=600, height=600, bd=2)
        self.frame1.grid(row=1, column=0)
        self.frame2 = tk.Frame(self.root, width=200, height=600, bd=1)
        self.frame2.grid(row=1, column=1)
        self.cv1 = tk.Canvas(self.frame1, height=590, width=590, background="white", bd=1, relief=tk.RAISED)
        self.cv1.grid(row=1,column=0)
        claButton = tk.Button(self.root, text='Previous', height=2, width=10, command=self.classify_obj)
        claButton.grid(row=0, column=1, padx=2, pady=2)
        broButton = tk.Button(self.root, text='Next', height=2, width=8, command = self.next_image)
        broButton.grid(row=0, column=0, padx=2, pady=2)
        fullButton = tk.Button(self.root, text='Watching full size', height=2, width=15, command = self.fullSize)
        fullButton.grid(row=1, column=1, padx=2, pady=2) 
        self.counter = 0
        self.max_count = len(self.list_images)-1
        self.next_image()

    def classify_obj(self):
        if self.counter < 0:
               mbox.showerror("Error", "Press Next Button to continue !!!")
        else:
            im = Image.open("{}{}".format("./TestImages/", self.list_images[self.counter]))
            if (590-im.size[0])<(590-im.size[1]):
                width = 590
                height = width*im.size[1]/im.size[0]
                self.pre_step(height, width)
            else:
                height = 590
                width = height*im.size[0]/im.size[1]
                self.pre_step(height, width)
    def pre_step(self, height, width):
        self.im = Image.open("{}{}".format("./TestImages/", self.list_images[self.counter-2]))
        self.im.thumbnail((width, height), Image.ANTIALIAS)
        self.root.photo = ImageTk.PhotoImage(self.im)
        self.photo = ImageTk.PhotoImage(self.im)
        if self.counter == 0:
            self.cv1.create_image(0, 0, anchor = 'nw', image = self.photo)
        else:
            self.im.thumbnail((width, height), Image.ANTIALIAS)
            self.cv1.delete("all")
            self.cv1.create_image(0, 0, anchor = 'nw', image = self.photo)
        self.counter -= 1
   
    def next_image(self):
        if self.counter > self.max_count:
           mbox.showerror("Error", "No more images !") 
        else:
            im = Image.open("{}{}".format("./TestImages/", self.list_images[self.counter]))
            if (590-im.size[0])<(590-im.size[1]):
                width = 590
                height = width*im.size[1]/im.size[0]
                self.next_step(height, width)
            else:
                height = 590
                width = height*im.size[0]/im.size[1]
                self.next_step(height, width)
    def next_step(self, height, width):
        self.im = Image.open("{}{}".format("./TestImages/", self.list_images[self.counter]))
        self.im.thumbnail((width, height), Image.ANTIALIAS)
        self.root.photo = ImageTk.PhotoImage(self.im)
        self.photo = ImageTk.PhotoImage(self.im)
        if self.counter == 0:
            self.cv1.create_image(0, 0, anchor = 'nw', image = self.photo)
        else:
            self.im.thumbnail((width, height), Image.ANTIALIAS)
            self.cv1.delete("all")
            self.cv1.create_image(0, 0, anchor = 'nw', image = self.photo)
        self.counter += 1
    def fullSize(self):
        window=tk.Toplevel()
        window.title(self.list_images[self.counter-1])
        self.mg = Image.open("{}{}".format("./TestImages/", self.list_images[self.counter]))
        w, h = Image.open("{}{}".format("./TestImages/", self.list_images[self.counter-1])).size
        window.geometry(("%dx%d+300+300") % (w, h))
        window.configure(background='grey')
        self.img = Image.open("{}{}".format("./TestImages/", self.list_images[self.counter-1]))
        img = ImageTk.PhotoImage(Image.open("{}{}".format("./TestImages/", self.list_images[self.counter-1])))
        panel = tk.Label(window, image = img)
        panel.pack(side="bottom", fill="both", expand=True)
        window.mainloop()

       
root = Tk()
root.geometry("800x500+300+300")
app = Example(root)
root.mainloop()
