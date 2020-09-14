import os
import tkinter as tk
from tkinter import filedialog, messagebox


class Application(tk.Frame):
    APP_HEIGHT = 300
    APP_WIDTH = 300
    def __init__(self, master=None):
        super().__init__(master)

        self._base_folder = os.path.dirname(__file__) + "/"
        self._master = master
        self.pack()

        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()
        position_right = int(self.winfo_screenwidth() / 2 - window_width / 2 - self.APP_WIDTH / 2)
        position_down = int(self.winfo_screenheight() / 2 - window_height / 2 - self.APP_HEIGHT / 2)
        self._master.geometry("{}x{}+{}+{}".format(self.APP_WIDTH, self.APP_HEIGHT, position_right, position_down))

        self.create_widgets()

        photo = tk.PhotoImage(file=self._base_folder + "favicon.png")
        self._master.iconphoto(False, photo)

        self.winfo_toplevel().title("Bagpipe Writer")

    def create_widgets(self):
        # https://realpython.com/python-gui-tkinter/
        """
        self.hi_there = tk.Button(self, text="Hello World\n(click me)", command=self.say_hi, width=15)
        self.hi_there.place(relx=0, rely=0)
        self.hi_there.pack(side="left")
        """

        self.filename_label = tk.Label(self)
        self.filename_label["text"] = "Current selected file: "
        #self.filename_label.place(x=0, y=0)
        self.filename_label.pack(side="left")

        self.filename = tk.Label(self)
        self.filename["text"] = "No .bww selected"
        #self.filename.place(x=0, y=0)
        self.filename.pack(side="left")








        frame1 = tk.Frame(master=self._master, height=100, bg="red")
        frame1.pack(fill=tk.X)

        frame2 = tk.Frame(master=self._master, height=50, bg="yellow", relief=tk.RAISED)
        frame2.pack(fill=tk.X)
        upload_button = tk.Button(master=frame2)
        upload_button["text"] = "Upload file ..."
        upload_button["command"] = self.upload_file
        # upload_button.place(relx=0, rely=0)
        upload_button.pack(fill=tk.X)
        # upload_button.place(x=100,y=100)

        self.save_button = tk.Button(master=frame2, state=tk.DISABLED)
        self.save_button["text"] = "Save ..."
        # .save_button.place(relx=100, rely=100)
        self.save_button.pack(fill=tk.X)

        quit_button = tk.Button(master=frame2, text="QUIT", fg="red", command=self.confirm_destroy)
        quit_button.place(relx=100, rely=10)
        quit_button.pack(fill=tk.X)


    def upload_file(self):
        file = filedialog.askopenfile(mode="r", filetypes=[('Bagpipe Player Files', "*.bww")])
        if file is not None:
            self.filename["text"] = os.path.basename(file.name)
            content = file.read()
            self.save_button["state"] = tk.NORMAL
            print(content)
        else:
            print("Nothing selected")

    def confirm_destroy(self):
        answer = tk.messagebox.askokcancel("Quit", "Are you sure you want to exit the application?", icon="warning")
        if answer:
            self.master.destroy()


root = tk.Tk()
app = Application(master=root)
app.mainloop()
