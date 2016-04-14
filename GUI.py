from tkinter import *
import tkinter.scrolledtext as tkst
from tkinter.ttk import *
from tkinter import messagebox  
from tkinter.font import Font, nametofont
#from PIL import Image, ImageTk
import datetime
import os

class textbox(Frame):
    def __init__(self, parent, orientation, message,
                                  bg_color='white'):
        Frame.__init__(self, parent)
        self.orientation = orientation
        self.bg_color = bg_color
        self.wraplength = 500
        self.set_style()
        #self.get_image()
        #self.set_image()
        self.row = 0
        self.font_size = 8
        self.message = message
        self.week = ['Sun',
                     'Mon',
                     'Tue',
                     'Wed',
                     'Thu',
                     'Fri',
                     'Sat']
        
        self.textbox_font = Font(family="MS Sans Serif",
                                 size=self.font_size)

        self.message_label = Label(self,
                                   text = self.message,
                                   background = self.bg_color,
                                   wraplength = self.wraplength)
    
        try:
            self.time_label = Label(self,
                                    text = self.get_time(),
                                    background = self.bg_color)
        except:
            messagebox.showinfo("Info", "Time not working")

        #self.image_label.pack(fill=BOTH)
        self.message_label.pack(fill=X)
        self.time_label.pack(fill=X, side=BOTTOM)

    #def get_image(self):
    #    self.background_image = image_url = 'chatbubble2.png'
    #    self.original_image = Image.open(os.path.join("images",
#                                                      image_url))
        
    #def size_image(self, size):
    #    resized = self.original_image.resize(size, Image.ANTIALIAS)
    #    self.background_image = ImageTk.PhotoImage(resized)
        
    
    def set_style(self):
        self.frame_style = Style()
        self.frame_style.configure('Canvas.TFrame',
                                   background=self.bg_color)
        self.style = 'Canvas.TFrame'

    #def set_image(self, image):
    #    if image == 1:
    #        image_url = 'chatbubble1.png'

     #   elif image == 2:
      #      image_url = 'chatbubble2.png'

        
    #    self._image = PhotoImage(file=os.path.join("images", image_url))
     #   self.image_label = Label(self,
     #                            image = self._image)
        

                                    
    def get_height(self):
        total_height = self.message_label.winfo_height() + self.time_label.winfo_height() + 12
        return total_height
    
    def get_time(self):
        current_time = datetime.datetime.now().time()
        c_hours = current_time.hour - 6
        c_minutes = current_time.minute
        meridiem = 'AM'

        
        if c_hours < 0:
            c_hours = 24 + c_hours
        
        if c_hours == 0:
            c_hours = 12
            
        if c_hours > 12:
            c_hours -= 12
            meridiem = 'PM'

        else:
            pass
        
        if c_minutes < 10:
            c_minutes = '0' + str(c_minutes)
                
        time_string = str(c_hours) + ':' + str(c_minutes) + ' ' +  \
                      meridiem
        return time_string


class GUI():
    def __init__(self, controller):
        self.controller = controller
        self.window = Toplevel()
        self.window.minsize(600, 400)
        self.window.geometry("600x400")
        self.window.title("Collab Messenger")
        self.window.protocol("WM_DELETE_WINDOW", self.exit_handler)
        self.text_empty = True
        self.default_entry_text = 'Write message here'
        self.default_text = True
        self.clicked = False
        self.font_size = 10
        self.entry_text = StringVar()
        self.create_top_menu()
        self.set_input_area()
        self.set_main_canvas()
        self.set_window_geometry()
        self.center_window()
        self.row = 0
        
    def create_top_menu(self):
        self.menu = Menu(self.window)

        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="New connection",
                                   command=self.temp_menu_func)
        
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit",
                                   command=self.exit_program)
        
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.options_menu = Menu(self.menu,
                                 tearoff=0)
        
        self.options_menu.add_command(label="Settings",
                                      command=self.temp_menu_func)
        
        self.menu.add_cascade(label="Options",
                              menu=self.options_menu)
         
        self.help_menu = Menu(self.menu, tearoff=0)
        
        self.help_menu.add_command(label="About",
                                   command=self.temp_menu_func)
        
        self.menu.add_cascade(label="Help",
                              menu=self.help_menu)

        self.window.config(menu=self.menu)

    def get_row(self):
        row = self.row
        self.row += 1
        return row
    
    def temp_menu_func(self):
        pass
    
    def center_window(self):
        self.window.update_idletasks()
        
        self.width = self.window.winfo_width()
        self.height = self.window.winfo_height()
        
        x = (self.window.winfo_screenwidth() // 2) - \
            (self.width // 2)
        y = (self.window.winfo_screenheight() // 2) - \
            (self.height // 2)
        
        self.window.geometry('{}x{}+{}+{}'.format(self.width,
                                           self.height,
                                           x, y))
        
        self.window.update()

    def set_window_geometry(self):
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

    
    def set_main_canvas(self):
        self.main_canvas_bounding_frame = Frame(self.window)
        self.main_canvas_bounding_frame.grid(row=0, column=0, sticky='news')
        self.main_canvas_bounding_frame.columnconfigure(0, weight=1)
        self.main_canvas_bounding_frame.rowconfigure(0, weight=1)
        
        canvas_style = Style()
        canvas_style.configure('Canvas.TFrame',
                               background = 'blue')

        
        self.main_canvas = Canvas(self.main_canvas_bounding_frame)
        self.main_canvas_frame = Frame(self.main_canvas, style ="Canvas.TFrame")
        #self.main_canvas_frame.columnconfigure(0, weight=1)
        
        self.window_scrollbar = Scrollbar(self.main_canvas_bounding_frame,
                                          command=self.main_canvas.yview)
        self.main_canvas.configure(yscrollcommand=self.window_scrollbar.set)
        
        self.window_scrollbar.pack(side="right", fill="y")
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.main_canvas.create_window((0,0), window=self.main_canvas_frame, anchor="nw",
                                       tags="self.main_canvas_frame")
        self.main_canvas_frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
    
    def set_input_area(self):
        self.input_area = Frame(self.window)
        self.input_area.columnconfigure(0, weight=1)
        self.window.bind('<Return>', self.on_return)
        self.send_button = Button(self.input_area,
                                  text = 'Send',
                                  command = self.send_message)
        
        self.toolkit_button = Button(self.input_area,
                                     text = 'Toolkit',
                                     command = self.show_toolkit)
        
        self.input_entry = tkst.ScrolledText(self.input_area,
                                             height=3, width=100,
                                             fg = "black")
        
        self.input_entry_font = Font(family="MS Sans Serif",
                                     size=self.font_size)
        
        self.input_entry.configure(font=self.input_entry_font)
        #self.input_entry.bind("<Button-1>",
        #                      self.click_inside_entry)
        
        self.send_button.grid(row=0, column=1)
        self.toolkit_button.grid(row=1, column=1)
        self.input_entry.grid(row=0, column=0,
                              rowspan=2, sticky='sew')
        self.input_area.grid(row=1, column=0, sticky='se')

        #s = Style()
        #s.configure('My.TFrame', background='red')
        self.input_area.configure(style='My.TFrame')

        #Set placeholder text
        #self.set_default_text()

    def message(self, title, message):
        '''Messagebox wrapper'''
        messagebox.showinfo(title, message)
        
    def disable_entry(self):
        self.input_entry.configure(state='disabled')
        self.send_button.configure(state='disabled')
        self.toolkit_button.configure(state='disabled')
        
    def enable_entry(self):
        self.input_entry.configure(state='normal')
        self.send_button.configure(state='normal')
        self.toolkit_button.configure(state='normal')
           
    def set_default_text(self):
        self.input_entry.delete('1.0', END)
        self.input_entry.insert(self.default_entry_text,
                                '1.0')

    def click_inside_entry(self, event):
        if self.clicked == False:
            self.clicked = True
            self.input_entry.delete('1.0', END)
            self.input_entry.configure(fg = 'black')
            
            
    def on_return(self, event):
        self.send_message()

    
    def get_spacer(self, parent):
        space_frame = Frame(parent)
        space_style = Style()
        space_style.configure('Space.TFrame',
                              background='green')
        
        space_frame.configure(style='Space.TFrame',
                              height=10)
        
        return space_frame
            
    def place_textbox(self, message, color='white'):
        message_frame = Frame(self.main_canvas_frame)
        space_frame = self.get_spacer(message_frame)
        space_frame.pack_propagate(0)
        space_frame.pack(fill=X)

        try:
            new_textbox = textbox(message_frame,
                                  'right',
                                  message,
                                  color)
        
        except:
            messagebox.showinfo("Error", "Error")

        new_textbox.pack(side=TOP, fill=X)
        
        message_frame.grid(row=self.get_row(), column=0, sticky='ew')

        self.window.update_idletasks()
        #Move main_canvas to bottom
        self.main_canvas.yview_moveto(1.0)
        
    def empty_text(self):
        if self.get_entry_text() in ("\n", "\r", " "):
            return True
        
        return False
        
    
    def get_entry_text(self):
        return self.input_entry.get('1.0', END)

        
    def clear_entry(self):
        self.input_entry.delete('1.0', END)
        
    def send_message(self):
        if not self.empty_text():
            self.place_textbox(self.get_entry_text())
            try:
                self.controller.send_message(self.get_entry_text())
            except:
                pass
            
            self.clear_entry()

    def receive_message(self, message):
        self.place_textbox(message, '#00ffff')

    def exit_handler(self):
        self.window.destroy()
        self.controller.cleanup()
        
    def wait_for_message(self):
        try:
            next_msg = self.controller.message_queue.get_nowait()
            self.place_textbox(next_msg.decode(), 2, '#00ffff')
            
        except:
            pass
        
        self.window.after(50, self.wait_for_message)
    
    def show_toolkit(self):
        pass

    def draw_graphics(self):
        pass

    def exit_program(self):
        response = messagebox.askyesno("Exit", "Are you sure you want to quit?")

        if response:
            self.exit_handler()

        else:
            pass
            
    
if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    gui = GUI()
    root.mainloop()
    
