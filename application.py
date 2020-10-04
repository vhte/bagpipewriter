import os
import tkinter
from tkinter import filedialog, messagebox


class Application(tkinter.Frame):
    APP_HEIGHT = 400
    APP_WIDTH = 450

    def __init__(self, bagpipe_writer):
        self._bagpipe_writer = bagpipe_writer

        super().__init__(tkinter.Tk())

        self._base_folder = os.path.dirname(__file__) + "/"
        self.pack()

        position_right = int(self.winfo_screenwidth() / 2 - self.winfo_reqwidth() / 2 - self.APP_WIDTH / 2)
        position_down = int(self.winfo_screenheight() / 2 - self.winfo_reqheight() / 2 - self.APP_HEIGHT / 2)
        self.master.geometry("{}x{}+{}+{}".format(self.APP_WIDTH, self.APP_HEIGHT, position_right, position_down))

        self.create_widgets()

        photo = tkinter.PhotoImage(file=self._base_folder + "favicon.png")
        self.master.iconphoto(False, photo)

        self.winfo_toplevel().title("Bagpipe Writer")

    def create_widgets(self):
        # https://realpython.com/python-gui-tkinter/

        self.filename_label = tkinter.Label(self)
        self.filename_label["text"] = "Current selected file: "
        #self.filename_label.place(x=0, y=0)
        self.filename_label.pack(side="left")

        self.filename = tkinter.Label(self)
        self.filename["text"] = "No .bww selected"
        #self.filename.place(x=0, y=0)
        self.filename.pack(side="left")


        frame1 = tkinter.Frame(master=self.master, height=100, bg="red")
        frame1.pack(fill=tkinter.X)

        frame2 = tkinter.Frame(master=self.master, height=50, bg="yellow", relief=tkinter.RAISED)
        frame2.pack(fill=tkinter.X)
        upload_button = tkinter.Button(master=frame2)
        upload_button["text"] = "Upload file ..."
        upload_button["command"] = self.upload_file
        # upload_button.place(relx=0, rely=0)
        upload_button.pack(fill=tkinter.X)
        # upload_button.place(x=100,y=100)

        self.save_button = tkinter.Button(master=frame2, state=tkinter.DISABLED)
        self.save_button["text"] = "Save ..."
        # .save_button.place(relx=100, rely=100)
        self.save_button.pack(fill=tkinter.X)

        self.run_button = tkinter.Button(master=frame2, state=tkinter.DISABLED)
        self.run_button["text"] = "Run"
        self.run_button.pack(fill=tkinter.X)

        quit_button = tkinter.Button(master=frame2, text="QUIT", fg="red", command=self.confirm_quit)
        quit_button.place(relx=100, rely=10)
        quit_button.pack(fill=tkinter.X)

        file_change_actions = [
            {
                "label": "Disable\nembellishments",
                "action": ""
            },
            {
                "label": "Disable\nrepetition",
                "action": ""
            },
            {
                "label": "Up all notes",
                "action": ""
            },
            {
                "label": "Down all notes",
                "action": ""
            },
            {
                "label": "Change tempo",
                "action": self.change_tempo
            },
            {
                "label": "Replace all\nembellishments",
                "action": ""
            },
            {
                "label": "Reset",
                "action": ""
            }
        ]

        i = 3
        for action in file_change_actions:
            if i == 3:
                frame = tkinter.Frame(
                    master=self.master,
                    relief=tkinter.RAISED,
                    borderwidth=0
                )
                frame.pack(padx=5, pady=5)
                i = 0

            label = tkinter.Button(master=frame, text=action["label"], command=action["action"])
            label.pack(padx=5, pady=5, side=tkinter.LEFT)
            i += 1

    def upload_file(self):
        file = filedialog.askopenfile(mode="r", filetypes=[('Bagpipe Player Files', "*.bww")])
        if file is not None:
            filename = os.path.basename(file.name)
            self.filename["text"] = filename
            self.save_button["state"] = tkinter.NORMAL
            self.run_button["state"] = tkinter.NORMAL

            self._bagpipe_writer.score = file.read()
            self._bagpipe_writer.filename = filename
            self._bagpipe_writer.new_file()

    def confirm_quit(self):
        answer = messagebox.askokcancel("Quit", "Are you sure you want to exit the application?", icon="warning")
        if answer:
            self.master.destroy()

    def change_tempo(self):
        tempo = self._bagpipe_writer.tempo
        print('called change_tempo: {}'.format(tempo))
