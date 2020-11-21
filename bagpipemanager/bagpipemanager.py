import os

from bagpipemanager.sheet import Sheet
from bagpipemanager.exceptions import BagpipeManagerException


class BagpipeManager:
    TMP_FILENAME = "tmp.bww"

    def __init__(self):
        self._filename = ""

        self._sheet = None

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, name):
        self._filename = name

    @property
    def score(self):
        return self._sheet.score

    @score.setter
    def score(self, content):
        self._sheet = Sheet(content)

    @property
    def tempo(self):
        return self._sheet.tempo

    @tempo.setter
    def tempo(self, value):
        self._sheet.tempo = value

    def save_tmp_file(self):
        if not self._filename or not self._sheet.score:
            raise ValueError("No filename or score set.")

        with open(self.TMP_FILENAME, "w") as file:
            file.write(self._sheet.score)

    def toggle_embellishments(self, disable):
        try:
            self._sheet.toggle_embellishments(disable)
        except BagpipeManagerException as e:
            pass  # TODO smooth passage to application

    def toggle_repetition(self, disable):
        self._sheet.toggle_repetition(disable)

    def clean_content(self):
        return self._sheet.clean_content()

    def __del__(self):
        if os.path.exists(self.TMP_FILENAME):
            os.remove(self.TMP_FILENAME)
