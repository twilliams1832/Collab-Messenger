from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import os


class ImageLabel:
    def __init__(self, master):
        self.master = master
        image_url = 'chatbubble2.png'
        self.original_image = Image.open(os.path.join("images",
                                                      image_url))
        
        resized = self.original_image.resize((50,50), Image.ANTIALIAS)
        self._image = ImageTk.PhotoImage(resized)
        
        self.image_label = Label(master,
                             image = self._image)
        
        self.image_label.pack(side=TOP)
        self.master.geometry("600x400")
        self.master.minsize(600, 400)
    
if __name__ == '__main__':
    root = Tk()
    label = ImageLabel(root)
    root.mainloop()
