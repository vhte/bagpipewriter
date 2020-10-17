import os
import re


class BagpipeManager:
    TMP_FILENAME = "tmp.bww"
    TUNE_TEMPO = "TuneTempo"

    def __init__(self):
        self._filename = ""
        self._score = ""

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, name):
        self._filename = name

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, content):
        self._score = content

    @property
    def tempo(self):
        tempo = re.findall(r"TuneTempo[\s]*,[\s]*(?P<tempo>[\d]+)", self._score)
        if tempo:
            return int(tempo[0])
        raise ValueError("Couldn't find {} in loaded score.".format(self.TUNE_TEMPO))

    @tempo.setter
    def tempo(self, value):
        pattern = re.compile(r"TuneTempo[\s]*,[\s]*[\d]+")
        self._score = pattern.sub("TuneTempo,{}".format(value), self._score)

    def save_tmp_file(self):
        if not self._filename or not self._score:
            raise ValueError("No filename or score set.")

        with open(self.TMP_FILENAME, "w") as file:
            file.write(self._score)

    def __del__(self):
        if os.path.exists(self.TMP_FILENAME):
            os.remove(self.TMP_FILENAME)
