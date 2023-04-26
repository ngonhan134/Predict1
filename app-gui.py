from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
from PIL import ImageTk, Image
#from gender_prediction import emotion,ageAndgender
from prediction import check
import threading
names = set()


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("PalmPrint Recognizer")
        self.resizable(False, False)
        self.geometry("500x250")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour,PageFive):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):

        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            f =  open("nameslist.txt", "a+")
            for i in names:
                    f.write(i+" ")
            self.destroy()


class StartPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            # load = Image.open("back1.png")
            # load = load.resize((250, 250), Image.ANTIALIAS)
            render = PhotoImage(file='back1.png')
            img = tk.Label(self, image=render)
            img.image = render
            img.grid(row=0, column=1, rowspan=4, sticky="nsew")
            label = tk.Label(self, text="        Home Page        ", font=self.controller.title_font,fg="#263942")
            label.grid(row=0, sticky="ew")
            button1 = tk.Button(self, text="   Add a User  ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageOne"))
            button2 = tk.Button(self, text="   Login  ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageTwo"))
            button3 = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff", command=self.on_closing)
            button1.grid(row=1, column=0, ipady=3, ipadx=7)
            button2.grid(row=2, column=0, ipady=3, ipadx=2)
            button3.grid(row=3, column=0, ipady=3, ipadx=32)


        def on_closing(self):
            if messagebox.askokcancel("Quit", "Are you sure?"):
                global names
                with open("nameslist.txt", "w") as f:
                    for i in names:
                        f.write(i + " ")
                self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Enter the name", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="#263942", command=self.start_training)
        self.buttoncanc.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)
    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        # self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")


# class PageTwo(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         self.scanning_label = tk.Label(self, text="Scanning...", fg="#263942", font='Helvetica 16 bold')
#         self.scanning_label.pack(pady=50)
#         self.result_label = tk.Label(self, text="", fg="#ff0000", font='Helvetica 12')
#         self.result_label.pack(pady=10)
#         self.thread = None
        

#         self.back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"), fg="#ffffff", bg="#263942")
#         self.back_button.pack(side="left", ipadx=5, ipady=4, pady=10)
#         self.scan_button = tk.Button(self, text="Scan", command=self.scan, fg="#ffffff", bg="#263942")
#         self.scan_button.pack(side="right", ipadx=5, ipady=4, pady=10)


#     def scan(self):
#         if self.thread is None or not self.thread.is_alive():
#             self.thread = threading.Thread(target=self.check_thread)
#             self.thread.start()
#     def check_thread(self):
#         if check():
#             self.controller.show_frame("PageFive")
#             self.back_button.place(x=10, y=self.winfo_height()-self.back_button.winfo_reqheight()-10)
#         else:
#             self.result_label.config(text="Not Access")   
#             self.after(3000, self.result_label.config, {'text': ''})

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Khai báo biến StringVar để hiển thị thông báo trên giao diện
        self.scanning_msg = tk.StringVar(value="Click 'Scan' to start scanning...") 
        self.scanning_label = tk.Label(self, textvariable=self.scanning_msg, fg="#263942", font='Helvetica 16 bold')
        self.scanning_label.pack(pady=50)
        self.result_label = tk.Label(self, text="", fg="#ff0000", font='Helvetica 12')
        self.result_label.pack(pady=10)
        self.thread = None
        self.back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"), fg="#ffffff", bg="#263942")
        self.back_button.pack(side="left", ipadx=5, ipady=4, pady=10)
        self.scan_button = tk.Button(self, text="Scan", command=self.scan, fg="#ffffff", bg="#263942")
        self.scan_button.pack(side="right", ipadx=5, ipady=4, pady=10)

    def scan(self):
        # Cập nhật lại giá trị của biến StringVar để hiển thị thông báo "Scanning..."
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.check_thread)
            self.thread.start()
        self.scanning_msg.set("Scanning...!!!!")
        self.update()  # Cập nhật giao diện ngay lập tức

    def check_thread(self):
        if check():
            self.controller.show_frame("PageFive")
            self.back_button.place(x=10, y=self.winfo_height()-self.back_button.winfo_reqheight()-10)
        else:
            self.result_label.config(text="Not Access")   
            self.after(3000, self.result_label.config, {'text': ''})

        # Cập nhật lại giá trị của biến StringVar để hiển thị lại thông báo ban đầu
        self.scanning_msg.set("Click 'Scan' to start scanning...")


# class PageTwo(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         self.scanning_label = tk.Label(self, text="Scanning...", fg="#263942", font='Helvetica 16 bold')
#         self.scanning_label.pack(pady=50)
#         self.result_label = tk.Label(self, text="", fg="#ff0000", font='Helvetica 12')
#         self.result_label.pack(pady=10)
        

#         self.back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"), fg="#ffffff", bg="#263942")
#         self.back_button.pack(side="left", ipadx=5, ipady=4, pady=10)
#         self.scan_button = tk.Button(self, text="Scan", command=self.start_scan_thread, fg="#ffffff", bg="#263942")
#         self.scan_button.pack(side="right", ipadx=5, ipady=4, pady=10)

#     def start_scan_thread(self):
#         # Khởi tạo một thread mới để thực hiện quá trình scan
#         scan_thread = threading.Thread(target=self.scan)
#         scan_thread.start()

#     def scan(self):
#         if check():
#             self.controller.show_frame("PageFive")
#             self.back_button.place(x=10, y=self.winfo_height()-self.back_button.winfo_reqheight()-10)
#         else:
#             self.result_label.config(text="Not Access")   
#             self.after(3000, self.result_label.config, {'text': ''})









class PageFive(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
    
        success_label = tk.Label(self, text="Verification Success!", font='Helvetica 24 bold', fg='blue')

        success_label.pack(pady=50)
        
        self.back_button = tk.Button(self, text="Back", command=self.go_back, fg="#ffffff", bg="#263942")
        self.back_button.pack(side="bottom", pady=10)
        
        self.bind("<Configure>", self.pack_configure)
        
    def go_back(self):
        self.controller.show_frame("PageTwo")
        
    def pack_configure(self, event):
        self.back_button.place(x=10, y=self.winfo_height()-self.back_button.winfo_reqheight()-10)


    # def display_image(self):
    #     img = Image.open("verify.png")
    #     img = img.resize((400, 400), Image.ANTIALIAS)
    #     photo = ImageTk.PhotoImage(img)
    #     self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    #     self.canvas.image = photo



class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#263942", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg="#263942",command=self.trainmodel)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 200 pic of your Palm.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 100:
            messagebox.showerror("ERROR", "No enough Data, Capture at least 200 images!")
            return
        train_classifer()
        # mp.freeze_support()
        # train_with_multi.main()
        # messagebox.showinfo("SUCCESS", "The modele has been successfully trained!")
        # self.controller.show_frame("PageTwo")
        messagebox.showinfo("SUCCESS", "The modele has been successfully trained!")
        self.controller.show_frame("PageTwo")


class PageFour(tk.Frame):   

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="PalmPrint Recognition", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        button1 = tk.Button(self, text=" Recognition", command=self.openwebcam, fg="#ffffff", bg="#263942")
        #button2 = tk.Button(self, text="Emotion Detection", command=self.emot, fg="#ffffff", bg="#263942")
        #button3 = tk.Button(self, text="Gender and Age Prediction", command=self.gender_age_pred, fg="#ffffff", bg="#263942")
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        #button2.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        #button3.grid(row=2,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        check(self.controller)




    #def gender_age_pred(self):
     #  ageAndgender()
    #def emot(self):
     #   emotion()



app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='hand.png'))
app.mainloop()


# class PageTwo(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         global names
#         self.controller = controller
#         tk.Label(self, text="Select user", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, padx=10, pady=10)
#         self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
#         self.menuvar = tk.StringVar(self)
#         self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
#         self.dropdown.config(bg="lightgrey")
        
        
#         self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
#         self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
#         self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)

#     def nextfoo(self):
#         if self.menuvar.get() == "None":
#             messagebox.showerror("ERROR", "Name cannot be 'None'")
#             return
#         self.controller.active_name = self.menuvar.get()
#         self.controller.show_frame("PageFour")

#     def refresh_names(self):
#         global names
#         self.menuvar.set('')
#         self.dropdown['menu'].delete(0, 'end')
#         for name in names:
#             self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))