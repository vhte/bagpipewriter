import os
import tkinter
import subprocess
from tkinter import filedialog, messagebox, simpledialog, PhotoImage


class Application(tkinter.Frame):
    APP_HEIGHT = 520
    APP_WIDTH = 450
    # TODO better approach to trigger bpplayer
    BAGPIPE_PLAYER = r"C:\Program Files (x86)\Bagpipe Player\BGPlayer.exe"

    def __init__(self, bagpipe_writer):
        self._bagpipe_writer = bagpipe_writer
        self._action_buttons = []
        self._original_score = ""

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

        self.master.protocol("WM_DELETE_WINDOW", self.confirm_quit)

    def create_widgets(self):
        # https://realpython.com/python-gui-tkinter/

        filename_label = tkinter.Label(self)
        filename_label["text"] = "Current selected file: "
        # filename_label.place(x=0, y=0)
        filename_label.pack(side="left")

        self.filename = tkinter.Label(self)
        self.filename["text"] = "No .bww selected"
        # self.filename.place(x=0, y=0)
        self.filename.pack(side="left")

        frame1 = tkinter.Frame(master=self.master, height=100)
        frame1.pack(fill=tkinter.X)
        fraser_logo = PhotoImage(file="fraser.png")
        fraser = tkinter.Label(master=frame1, image=fraser_logo)
        fraser.photo = fraser_logo
        fraser.pack()

        frame2 = tkinter.Frame(master=self.master, height=50, bg="yellow", relief=tkinter.RAISED)
        frame2.pack(fill=tkinter.X)
        upload_button = tkinter.Button(master=frame2)
        upload_button["text"] = "Upload file ..."
        upload_button["command"] = self.upload_file
        # upload_button.place(relx=0, rely=0)
        upload_button.pack(fill=tkinter.X)
        # upload_button.place(x=100,y=100)

        self.save_button = tkinter.Button(master=frame2, state=tkinter.DISABLED, command=self.save)
        self.save_button["text"] = "Save ..."
        # .save_button.place(relx=100, rely=100)
        self.save_button.pack(fill=tkinter.X)

        self.run_button = tkinter.Button(master=frame2, state=tkinter.DISABLED, command=self.run)
        self.run_button["text"] = "Run"
        self.run_button.pack(fill=tkinter.X)

        about_button = tkinter.Button(master=frame2, text="About", fg="red")
        about_button.place(relx=100, rely=10)
        about_button.pack(fill=tkinter.X)

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
                "action": self.reset
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

            button = tkinter.Button(master=frame, text=action["label"], command=action["action"], state=tkinter.DISABLED)
            button.pack(padx=5, pady=5, side=tkinter.LEFT)
            self._action_buttons.append(button)
            i += 1

    def upload_file(self):
        file = filedialog.askopenfile(mode="r", filetypes=[('Bagpipe Player Files', "*.bww")])
        if file is not None:
            filename = os.path.basename(file.name)
            self.filename["text"] = filename
            self.save_button["state"] = tkinter.NORMAL
            self.run_button["state"] = tkinter.NORMAL
            for button in self._action_buttons:
                button["state"] = tkinter.NORMAL

            self._original_score = self._bagpipe_writer.score = file.read()
            self._bagpipe_writer.filename = filename
            self._bagpipe_writer.save_tmp_file()

    def confirm_quit(self):
        answer = messagebox.askokcancel("Quit", "Are you sure you want to exit the application?\nAll unsaved data will be lost.", icon="warning")
        if answer:
            self.master.destroy()

    def change_tempo(self):
        try:
            tempo = self._bagpipe_writer.tempo
        except IndexError as index_error:
            print("Error while retrieving tune tempo: {}".format(index_error))
            return

        print('called change_tempo: {}'.format(tempo))
        new_value = simpledialog.askinteger("Change Tempo", "New value", parent=self, minvalue=0, maxvalue=200, initialvalue=tempo)
        if new_value:
            print("New tempo is: {}".format(new_value))
            self._bagpipe_writer.tempo = new_value

            self.run_button.focus_set()

    def save(self):
        file = filedialog.asksaveasfile(filetypes=[('Bagpipe Player Files', "*.bww")], defaultextension=".bww", initialfile=self.filename["text"].replace(".bww", "_mod.bww"))
        if file:
            file.write(self._bagpipe_writer.score)
            file.close()

    def run(self):
        self._bagpipe_writer.save_tmp_file()
        subprocess.Popen([self.BAGPIPE_PLAYER, self._bagpipe_writer.TMP_FILENAME])

    def reset(self):
        if messagebox.askyesno("Confirm action", "Reset ALL modifications?"):
            self._bagpipe_writer.score = self._original_score
