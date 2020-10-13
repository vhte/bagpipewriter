import os


class BagpipeWriter:
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
        tune_tempo = self._score.find(self.TUNE_TEMPO)
        if tune_tempo == -1:
            raise IndexError("No {} was found in the file.".format(self.TUNE_TEMPO))

        start = tune_tempo + len(self.TUNE_TEMPO)

        # TODO regex
        return int(self._score[start:].split(",")[1].rsplit("\n")[0])

    @tempo.setter
    def tempo(self, value):
        # TODO regex
        pattern = "TuneTempo,{}"
        self._score = self._score.replace(pattern.format(str(self.tempo)), pattern.format(value))

    def save_tmp_file(self):
        if not self._filename or not self._score:
            raise ValueError("No filename or score set.")

        with open(self.TMP_FILENAME, "w") as file:
            file.write(self._score)

    def __del__(self):
        if os.path.exists(self.TMP_FILENAME):
            os.remove(self.TMP_FILENAME)
