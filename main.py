#!/usr/bin/python3

# Su dung thu vien Tkinter de lap trinh GUI.

from tkinter import Tk, W, NW, Text, TOP, BOTH, Canvas, X, N, LEFT, RIGHT, BOTTOM, RAISED, Menu
from tkinter.filedialog import Open 
from tkinter import Frame, Label, Button, Entry#, Style
from tkinter.ttk import Style 
from PIL import Image
from PIL import ImageTk
import tkinter.messagebox as mbox
from tkinter.colorchooser import askcolor
import tkinter as tk
import os
import shutil
import numpy
from fpdf import FPDF
from datetime import datetime 
from queue import Queue
from threading import Thread
from myQueue import do_stuff

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.threading_start = None
        self.queue = Queue()
        self.initUI()

    def initUI(self):
        self.parent.title("Facebook searching tool")
        self.style = Style()
        self.style.theme_use("classic")
        self.pack(fill=BOTH, expand=1)
        frame1 = Frame(self)
        frame1.pack(fill=X)
        lbl1 = Label(frame1, text="Facebook searching tool !!!", font="VNI-Dom 15", width=50, foreground="blue")
        lbl1.pack(side=TOP, padx=8, pady=8, expand=True) 
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        
        fileMenu = Menu(menubar)       
        submenu = Menu(fileMenu)
        submenu.add_command(label="Watch result Button", command=self.onChoose2)
        submenu.add_command(label="Stop Button", command=self.onChoose3)
        submenu.add_command(label="Start Button", command=self.onChoose5)
        submenu.add_command(label="Extract Button", command=self.onChoose1)
        submenu.add_command(label="Background", command=self.onChoose6)
        
        fileMenu.add_cascade(label='Change colour', menu=submenu)
        fileMenu.add_separator()
        fileMenu.add_command(label="Go to the result folder", command=self.onOpen)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Option", menu=fileMenu)        

        frame1 = Frame(self)
        frame1.pack(fill=X)
        lbl1 = Label(frame1, text="Key word",font="VNI-Dom 12", foreground="black", width=13)
        lbl1.pack(side=LEFT, padx=18, pady=12)
        self.entry1 = Entry(frame1)
        self.entry1.insert(0,'i want this shirt')
        self.entry1.pack(fill=X, padx=5, expand=True)

        frame2 = Frame(self)
        frame2.pack(fill=X)
        lbl2 = Label(frame2, text="Extract file",font="VNI-Dom 12", foreground="black", width=13)
        lbl2.pack(side=LEFT, padx=18, pady=12)
        self.entry2 = Entry(frame2)
        self.entry2.pack(fill=X, padx=5, expand=True)

        # bard = Image.open("28.jpg")
        # bardejov = ImageTk.PhotoImage(bard)
        # label1 = Label(self, image=bardejov)
        # label1.image = bardejov
        # label1.pack(side=BOTTOM, padx=10, expand=True)

        self.quitButton = Button(self, text="Quit", height=1, width=10, command=self.onQuest, background="black", foreground="white")
        self.quitButton.pack(side=RIGHT, padx=5, pady=5)
        self.newkeywordButton = Button(self, text="Delete key word", height=1, width=10, command=self.onDeleteentry, background="red", foreground="white")
        self.newkeywordButton.pack(side=RIGHT, padx=5, pady=5)
        self.deleteresultButton = Button(self, text="Delete result", height=1, width=10, command=self.deleteAllfile, background="red", foreground="white")
        self.deleteresultButton.pack(side=RIGHT, padx=5, pady=5)
        self.extractButton = Button(self, text="Extract", height=1, width=10, command=self.outFile, background="black", foreground="white")
        self.extractButton.pack(side=RIGHT, padx=5, pady=5)
        self.okButton1 = Button(self, text="Watch result", height=1, width=10, command=self.onshowImages, background="green", foreground="white")
        self.okButton1.pack(side=RIGHT, padx=5, pady=5)
        self.closeButton = Button(self, text="Stop", height=1, width=10, command=self.onStop, background="green", foreground="white")
        self.closeButton.pack(side=RIGHT, padx=5, pady=5)
        self.okButton = Button(self, text="Start", height=1, width=10, command=self.onStartentry, background="green", foreground="white")
        self.okButton.pack(side=RIGHT, padx=5, pady=5)

    def onQuest(self):
        outButton = mbox.askquestion("Question", "Are you sure to quit ?")
        if outButton == "yes":
            for i in range(1, 10):
                self.quit()

    def onStop(self):
        stopButton = mbox.askquestion("Question", "Do you want to stop ?")
        if stopButton == 'yes':
            setattr(self.queue, 'do_run', False)
            os.system("TASKKILL /F /IM firefox.exe")
            self.okButton.config(state=tk.NORMAL)

    def process_queue(self):
        self.queue = Queue(maxsize=0)
        num_threads = 5
        for i in range(num_threads):
            worker = Thread(target=do_stuff, args=(self.queue,))
            worker.setDaemon(True)
            worker.start()
        for x in range(50):
            self.queue.put(x)
        self.queue.join()
        self.okButton.config(state=tk.NORMAL)

    def onStartentry(self):
        # outButton = mbox.askquestion("Question", "Do you want to remove old images before start ?")
        # if outButton == "yes":
        #   src = "./IM/"
        #   for d in os.listdir(src):
        #     sublink="{}{}".format(src,d)
        #     os.remove(sublink)
        key_word = self.entry1.get()
        self.threading_start = Thread(target=self.process_queue)
        self.threading_start.setDaemon(True)
        self.threading_start.start()
        self.okButton.config(state=tk.DISABLED)

    def onOpen(self):
        ftypes = {('All files', '*'), ('Text files', '*.txt'), ('jpg file', '*.jpg'), ('gif file', '*.gif')}
        dlg = Open(self, filetypes=ftypes)
        fl = dlg.show()
        if fl != '':
            images = fl
            if images.endswith("png") \
                or images.endswith("jpg") \
                or images.endswith("jpeg") \
                or images.endswith("gif") \
                or images.endswith("tiff") \
                or images.endswith("bmp") \
                or images.endswith("PNG") \
                or images.endswith("JPG") \
                or images.endswith("JPEG") \
                or images.endswith("GIF") \
                or images.endswith("TIFF") \
                or images.endswith("BMP"):
                window=tk.Toplevel()
                str = fl.split('/', 100)
                number_last = len(fl.split('/', 100)) - 1
                window.title(str[number_last])
                self.mg = Image.open(fl)
                w, h = Image.open(fl).size
                window.geometry(("%dx%d + 300 + 300") % (w, h))
                window.configure(background='grey')
                path= fl 
                self.img = Image.open(path)
                img = ImageTk.PhotoImage(Image.open(path))
                panel = tk.Label(window, image = img)
                panel.pack(side="bottom", fill="both", expand=True)
                window.mainloop()
            else:
                mbox.showerror("Error", "Could not open file")

    def onChoose1(self):
                (rgb, hx) = askcolor()
                self.extractButton.config(bg=hx)

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

    def deleteAllfile(self):
            outButton = mbox.askquestion("Question", "Do you want to remove all images ?")
            if outButton == "yes":
                    src = "./IM/"
                    for d in os.listdir(src):
                            sublink="{}{}".format(src,d) 
                            os.remove(sublink) 

    def outFile(self):
            link=self.entry2.get()
            src = "./TestImages/"
            self.list_images = []
            pdf = FPDF('p','mm','A4')
            x,y,w,h=0,0,200,250
            for d in os.listdir(src):
                images = d
                if (images.endswith("png") or images.endswith("jpg") 
                    or images.endswith("jpeg") 
                    or images.endswith("gif") 
                    or images.endswith("tiff") 
                    or images.endswith("bmp") 
                    or images.endswith("PNG") 
                    or images.endswith("JPG") 
                    or images.endswith("JPEG") 
                    or images.endswith("GIF") 
                    or images.endswith("TIFF") 
                    or images.endswith("BMP")):
                    sublink="{}{}".format("./TestImages/",d) 
                    shutil.copy(sublink, link) 
                    pdf.add_page()
                    pdf.image(sublink,x,y,w,h)
            now = datetime.now()
            current_year = now.year
            current_month = now.month
            current_day = now.day
            curent_hour = now.hour
            current_minute = now.minute
            current_second = now.second
            date_time = "Reportimages_%s_%s_%s_%s_%s_%s" % (current_year, current_month, current_day, curent_hour, current_minute, current_second)
            outlink = "{}{}".format(link,date_time)
            pdf.output(outlink, "F") 

    def onDeleteentry(self):
            self.entry1.delete(0, 10000)

    def onshowImages(self):
            root = tk.Toplevel() 
            MyApp = ImageClassifyer(root)
            tk.mainloop()

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
        self.frame2 = tk.Frame(self.root, width=600, height=50, bd=1)
        self.frame2.grid(row=3, column=0)
        self.frame3 = tk.Frame(self.root, width=600, height=50, bd=1)
        self.frame3.grid(row=4, column=0)
        self.frame4 = tk.Frame(self.root, width=600, height=50, bd=1)
        self.frame4.grid(row=2, column=0)
        self.cv1 = tk.Canvas(self.frame1, height=590, width=590, background="white", bd=1, relief=tk.RAISED)
        self.cv1.grid(row=1,column=0)
        lbl1 = Label(self.frame2, text="Like",font="VNI-Dom 12", foreground="black", width=7)
        lbl1.pack(side=LEFT, padx=1, pady=1)
        self.entry1 = Entry(self.frame2, width=8)
        self.entry1.pack(side=LEFT, padx=1, pady=1)
        lbl2 = Label(self.frame2, text="Share",font="VNI-Dom 12", foreground="black", width=7)
        lbl2.pack(side=LEFT, padx=1, pady=1)
        self.entry2 = Entry(self.frame2, width=8)
        self.entry2.pack(side=LEFT, padx=1, pady=1)
        lbl3 = Label(self.frame2, text="Comment",font="VNI-Dom 12", foreground="black", width=9)
        lbl3.pack(side=LEFT, padx=1, pady=1)
        self.entry3 = Entry(self.frame2, width=8)
        self.entry3.pack(side=LEFT, padx=1, pady=1)
        lbl4 = Label(self.frame4, text="File name",font="VNI-Dom 12", foreground="black", width=9)
        lbl4.pack(side=LEFT, padx=1, pady=1)
        self.entry4 = Entry(self.frame4, width=42)
        self.entry4.pack(side=LEFT, padx=1, pady=1)

        broButton = tk.Button(self.frame3, text='Next', height=1, width=7, command = self.next_image, background="green", foreground="white")
        broButton.pack(side = LEFT)
        claButton = tk.Button(self.frame3, text='Previous', height=1, width=7, command=self.classify_obj, background="green", foreground="white")
        claButton.pack(side = LEFT)
        fullButton = tk.Button(self.frame3, text='Full size', height=1, width=7, command = self.fullSize, background="black", foreground="white")
        fullButton.pack(side = LEFT)
        deleteButton = tk.Button(self.frame3, text='Delete', height=1, width=7, command = self.deleteImages, background="red", foreground="white")
        deleteButton.pack(side = LEFT)

        self.counter = 0
        self.max_count = len(self.list_images)-1
        self.next_image()
        print("max count: %s", self.max_count)

    def classify_obj(self):
        if self.counter < 0:
            print("self tai previu: %s", self.counter)
            self.counter =0 
            mbox.showerror("Error", "Press Next Button to continue !!!")
        elif self.counter > self.max_count:
            self.counter =  self.max_count 
        else: 
            if self.counter > self.max_count:
                        self.counter =  self.max_count
            fl = self.list_images[self.counter]
            str = fl.split('_', 1000)
            number_comment = len(fl.split('_', 1000)) - 1
            number_share = number_comment - 1
            number_like = number_comment - 2
            str1 = str[number_comment].split('.', 1000)
            comment = str1[0]
            share = str[number_share]
            like = str[number_like]
            self.entry1.delete(0, 10000)
            self.entry2.delete(0, 10000)
            self.entry3.delete(0, 10000)
            self.entry1.insert(0, like)
            self.entry2.insert(0, share)
            self.entry3.insert(0, comment)
            self.entry4.delete(0, 10000)
            self.entry4.insert(0, self.list_images[self.counter])

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
            # self.counter = self.max_count
            mbox.showerror("Error", "No more images !") 
        else:
            fl = self.list_images[self.counter]
            str = fl.split('_', 1000)
            number_comment = len(fl.split('_', 1000)) - 1
            number_share = number_comment - 1
            number_like = number_comment - 2
            str1 = str[number_comment].split('.', 1000)
            comment = str1[0]
            share = str[number_share]
            like = str[number_like]
            self.entry1.delete(0, 10000)
            self.entry2.delete(0, 10000)
            self.entry3.delete(0, 10000)
            self.entry1.insert(0, like)
            self.entry2.insert(0, share)
            self.entry3.insert(0, comment)
            self.entry4.delete(0, 10000)
            self.entry4.insert(0, self.list_images[self.counter]) 
            im = Image.open("{}{}".format("./TestImages/", self.list_images[self.counter]))
            if (590-im.size[0])<(590-im.size[1]):
                width = 590
                height = width*im.size[1]/im.size[0]
                self.next_step(height, width)
            else:
                height = 590
                width = height*im.size[0]/im.size[1]
                self.next_step(height, width)
            print(self.counter)

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

    def deleteImages(self):
        os.remove("{}{}".format("./TestImages/", self.list_images[self.counter-1]))
        self.list_images = numpy.delete(self.list_images, self.counter-1)
        self.counter = self.counter-1       
        self.max_count = len(self.list_images)-1

root = Tk()
root.geometry("800x300+300+300")
app = Example(root)
root.mainloop()
