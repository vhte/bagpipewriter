import os
import tkinter as tk
from tkinter import filedialog, messagebox


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self._base_folder = os.path.dirname(__file__) + "/"
        self._master = master
        self.pack()
        self.create_widgets()
        photo = tk.PhotoImage(file=self._base_folder + "favicon.png")
        self._master.iconphoto(False, photo)

        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()
        position_right = int(self.winfo_screenwidth() / 2 - window_width / 2) - 150
        position_down = int(self.winfo_screenheight() / 2 - window_height / 2) - 150
        self._master.geometry("300x300+{}+{}".format(position_right, position_down))

        self.winfo_toplevel().title("Test")

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.upload_button = tk.Button(self)
        self.upload_button["text"] = "Upload file ..."
        self.upload_button["command"] = self.upload_file
        self.upload_button.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        messagebox.showerror("Title", "this is an error!")
        print("hi there, everyone!")

    def upload_file(self):
        filename = filedialog.askopenfile()
        print("Selected: {}".format(filename))


root = tk.Tk()
app = Application(master=root)
app.mainloop()
