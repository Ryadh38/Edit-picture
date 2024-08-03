import random
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image, ImageFilter

BLUR = ImageFilter.BLUR

filters_bib = ["BLUR","CONTOUR","DETAIL","EDGE_ENHANCE","EDGE_ENHANCE_MORE","EMBOSS","FIND_EDGES","SHARPEN","SMOOTH","SMOOTH_MORE"]

class ImageEdit(tk.Tk):
    def __init__(self, *args, **kw):
        print(globals())
        super().__init__(*args, **kw)
        self.geometry("600x400")
        self.title("ShotoPhop")
        self.path = tk.StringVar()
        tk.Label(self, text="file (full path) :").place(x="25", y=f"25")
        tk.Entry(self, width=50, textvariable=self.path).place(x="150", y="25")
        tk.Button(self, text="Load", command=self.load).place(x="480", y="25")
        self.can = tk.Canvas(self, width=300, height=300, bg="grey")
        self.can.place(x="250", y="60")

        self.filters_check = {}
        for i, fltr in enumerate(filters_bib):
            y = 70 + 25 * i
            self.filters_check[fltr] = tk.BooleanVar()
            tk.Label(self, text=fltr).place(x="70", y=f"{y}")
            tk.Checkbutton(self, offvalue=False, onvalue=True, variable=self.filters_check[fltr]).place(x="30", y=f"{y}")


        tk.Button(self, text="Apply", command=self.apply).place(x="60", y="340")
        tk.Button(self, text="Save", command=self.save).place(x="130", y="340")

        self.img = None

        self.image_to_save = None

    def load(self):
        if self.path.get() == "":
            tk.messagebox.showerror('Error', f'Error: Empty file name !')
        else:
            try:
                self.img = Image.open(self.path.get())
            except FileNotFoundError:
                print("not found")
                tk.messagebox.showerror('Error', f'Error: There is no file named "{self.path.get()}" !')
            else:
                self.photoimg = ImageTk.PhotoImage(self.img)
                self.can.create_image(0, 0, image=self.photoimg)

    def apply(self):
        if self.img != None:
            img = self.img
            for key, value in self.filters_check.items():
                if value.get():
                    img = img.filter(getattr(ImageFilter, key))

            self.image_to_save = img
            self.photoimg = ImageTk.PhotoImage(img)
            self.can.create_image(0, 0, image=self.photoimg)

    def save(self):
        rnd = 0
        for i in range(1, 10):
            rnd += random.randint(0,9)
            rnd *= 10
        if self.image_to_save != None:
            self.image_to_save.save(f"{str(rnd)}.jpg", "JPEG")