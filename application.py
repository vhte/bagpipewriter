import os
import tkinter
import subprocess
from webbrowser import open_new
from tkinter import filedialog, messagebox, simpledialog, PhotoImage

__version__ = "0.0.1a"


class Application(tkinter.Frame):
    APP_HEIGHT = 505
    APP_WIDTH = 450
    DISABLED_BACKGROUND = "#FFA8A4"
    ENABLED_BACKGROUND = "#78FF85"
    # TODO better approach to trigger bpplayer
    BAGPIPE_PLAYER = r"C:\Program Files (x86)\Bagpipe Player\BGPlayer.exe"

    def __init__(self, bagpipe_manager):
        self._bagpipe_manager = bagpipe_manager
        self._action_buttons = []
        self._original_score = ""

        super().__init__(tkinter.Tk())

        self._base_folder = os.path.dirname(__file__) + "/"
        self.pack()

        self.master.geometry(self._center_window(self.APP_WIDTH, self.APP_HEIGHT))

        self.create_widgets()

        photo = tkinter.PhotoImage(file=self._base_folder + "favicon.png")
        self.master.iconphoto(True, photo)

        self.winfo_toplevel().title("Bagpipe Manager")
        self.master.resizable(0, 0)

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
        frame1.pack()
        fraser_logo = PhotoImage(file="fraser.png")
        fraser = tkinter.Label(master=frame1, image=fraser_logo)
        fraser.photo = fraser_logo
        fraser.pack()

        frame2 = tkinter.Frame(master=self.master, bg="yellow", relief=tkinter.RAISED)
        frame2.pack(fill=tkinter.X)
        upload_button = tkinter.Button(master=frame2, text="Upload file ...", command=self.upload_file)
        upload_button.pack(fill=tkinter.X)

        self.save_button = tkinter.Button(
            master=frame2, state=tkinter.DISABLED, command=self.save, text="Save ..."
        )
        self.save_button.pack(fill=tkinter.X)

        self.run_button = tkinter.Button(
            master=frame2, state=tkinter.DISABLED, command=self.run, fg="red", text="Run"
        )
        self.run_button.pack(fill=tkinter.X)

        about_button = tkinter.Button(master=frame2, text="About", command=self.about)
        about_button.place(relx=100, rely=10)
        about_button.pack(fill=tkinter.X)

        separator = tkinter.Frame(height=2)  # relief=tkinter.SUNKEN
        separator.pack(fill=tkinter.X, padx=5, pady=5)

        # generates self._action_buttons
        file_change_actions = [
            {
                "id": "toggle_embellishments",
                "label": "Embellishments\nOFF",
                "action": self.toggle_embellishments,
                "initial_background": self.DISABLED_BACKGROUND,
            },
            {
                "id": "toggle_repetition",
                "label": "Repetition\nOFF",
                "action": self.toggle_repetition,
                "initial_background": self.DISABLED_BACKGROUND,
            },
            {"id": "up_all_notes", "label": "Up all\nnotes", "action": self.up_all_notes},
            {"id": "down_all_notes", "label": "Down all\nnotes", "action": self.down_all_notes},
            {
                "id": "change_tempo",
                "label": "Change\ntempo",
                "action": self.change_tempo,
            },
            {"id": "reset", "label": "Reset", "action": self.reset},
        ]

        i = 4
        for action in file_change_actions:
            if i == 4:
                frame = tkinter.Frame(
                    master=self.master, relief=tkinter.RAISED, borderwidth=0, bg=None
                )
                frame.pack(padx=5, pady=5)
                i = 0

            button = tkinter.Button(
                master=frame,
                text=action["label"],
                command=action["action"],
                state=tkinter.DISABLED,
            )
            button.pack(padx=5, pady=5, side=tkinter.LEFT)
            self._action_buttons.append(
                {
                    "id": action["id"],
                    "object": button,
                    "properties": {
                        "background": ""
                        if "initial_background" not in action
                        else action["initial_background"]
                    },
                }
            )
            i += 1

        frame3 = tkinter.Frame(master=self.master, bg=None, relief=tkinter.RAISED)
        frame3.pack(fill=tkinter.X)
        version_label = tkinter.Label(master=frame3)
        version_label["text"] = "{}: {}".format("version", __version__)
        version_label.pack(side="right", padx=5, pady=0)

    def upload_file(self):
        file = filedialog.askopenfile(
            mode="r", filetypes=[("Bagpipe Player Files", "*.bww")]
        )
        if file is not None:
            filename = os.path.basename(file.name)
            self.filename["text"] = filename
            self.save_button["state"] = tkinter.NORMAL
            self.run_button["state"] = tkinter.NORMAL
            for button in self._action_buttons:
                button["object"]["state"] = tkinter.NORMAL
                if button["properties"]["background"]:
                    button["object"]["background"] = button["properties"]["background"]
                    button["object"]["activebackground"] = button["properties"][
                        "background"
                    ]

            self._original_score = self._bagpipe_manager.score = file.read()
            self._bagpipe_manager.filename = filename
            self._bagpipe_manager.save_tmp_file()

    def confirm_quit(self):
        if self._original_score:
            answer = messagebox.askokcancel(
                "Quit",
                "Leave application?\nAll unsaved data will be lost.",
                icon="warning",
            )
            if answer:
                self.master.destroy()
        else:
            self.master.destroy()

    def change_tempo(self):
        try:
            tempo = self._bagpipe_manager.tempo
        except IndexError as index_error:
            print("Error while retrieving tune tempo: {}".format(index_error))
            return

        new_value = simpledialog.askinteger(
            "Change Tempo",
            "New value",
            parent=self,
            minvalue=0,
            maxvalue=200,
            initialvalue=tempo,
        )
        if new_value:
            self._bagpipe_manager.tempo = new_value

            self.run_button.focus_set()

    def save(self):
        file = filedialog.asksaveasfile(
            filetypes=[("Bagpipe Player Files", "*.bww")],
            defaultextension=".bww",
            initialfile=self.filename["text"].replace(".bww", "_mod.bww"),
        )
        if file:
            file.write(self._bagpipe_manager.clean_content())
            file.close()

    def run(self):
        self._bagpipe_manager.save_tmp_file()
        subprocess.Popen([self.BAGPIPE_PLAYER, self._bagpipe_manager.TMP_FILENAME])

    def reset(self):
        if messagebox.askyesno("Confirm action", "Reset ALL modifications?"):
            self._bagpipe_manager.score = self._original_score

    def toggle_embellishments(self):
        button = self._get_button("toggle_embellishments")
        if button["object"]["background"] == self.ENABLED_BACKGROUND:
            # Disable
            self._bagpipe_manager.toggle_embellishments(False)
            button["object"]["background"] = self.DISABLED_BACKGROUND
            button["object"]["text"] = "Embellishments\nOFF"
            button["object"]["activebackground"] = self.DISABLED_BACKGROUND
        else:
            # Enable
            self._bagpipe_manager.toggle_embellishments(True)
            button["object"]["background"] = self.ENABLED_BACKGROUND
            button["object"]["text"] = "Embellishments\nON"
            button["object"]["activebackground"] = self.ENABLED_BACKGROUND

    def toggle_repetition(self):
        button = self._get_button("toggle_repetition")
        if button["object"]["background"] == self.ENABLED_BACKGROUND:
            # Disable
            self._bagpipe_manager.toggle_repetition(False)
            button["object"]["background"] = self.DISABLED_BACKGROUND
            button["object"]["text"] = "Repetition\nOFF"
            button["object"]["activebackground"] = self.DISABLED_BACKGROUND
        elif button["object"]["background"] == self.DISABLED_BACKGROUND:
            # Enable
            self._bagpipe_manager.toggle_repetition(True)
            button["object"]["background"] = self.ENABLED_BACKGROUND
            button["object"]["text"] = "Repetition\nON"
            button["object"]["activebackground"] = self.ENABLED_BACKGROUND

    def up_all_notes(self):
        alert = self._bagpipe_manager.jump_notes(True)
        if alert:
            messagebox.showwarning("Warning", alert)

    def down_all_notes(self):
        alert = self._bagpipe_manager.jump_notes(False)
        if alert:
            messagebox.showwarning("Warning", alert)

    def _get_button(self, _id):
        return next(button for button in self._action_buttons if button["id"] == _id)

    def about(self):
        window = tkinter.Toplevel(self.master)
        window.title("About")
        window_width = 340
        window_height = 100
        window.geometry(self._center_window(window_width, window_height))
        tkinter.Label(
            window, text="{} {}".format("Bagpipe Manager", __version__)
        ).place(x=10, y=10, anchor=tkinter.NW)

        tkinter.Label(window, text="Victor Torres  -").place(
            x=10, y=30, anchor=tkinter.NW
        )

        link1 = tkinter.Label(
            window,
            text="https://github.com/vhte/bagpipemanager",
            fg="blue",
            cursor="hand2",
        )
        link1.place(x=92, y=30, anchor=tkinter.NW)
        link1.bind(
            "<Button-1>", lambda e: open_new("https://github.com/vhte/bagpipemanager")
        )

        close_button = tkinter.Button(master=window, width=8, text="Close", command=window.destroy)
        close_button.place(x=142, y=60, anchor=tkinter.NW)

        window.resizable(0, 0)
        window.focus_set()
        window.grab_set()

    def _center_window(self, window_width, window_height):
        position_right = int(
            self.winfo_screenwidth() / 2
            - self.winfo_reqwidth() / 2
            - window_width / 2
        )
        position_down = int(
            self.winfo_screenheight() / 2
            - self.winfo_reqheight() / 2
            - window_height / 2
        )

        return "{}x{}+{}+{}".format(window_width, window_height, position_right, position_down)