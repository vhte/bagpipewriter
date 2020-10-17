import re


class Sheet:
    TUNE_TEMPO = "TuneTempo"

    def __init__(self, score="", tempo=0):
        self._score = score
        self._tempo = tempo

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
        
    def toggle_repetition(self, disable):
        # TODO improve sub() use
        if disable is True:
            pattern = re.compile(r"(I!'')")
            self._score = pattern.sub("I!\"'''\"", self._score)
            pattern = re.compile(r"(''!I)")
            self._score = pattern.sub("\"'''\"\n!I", self._score)
        else:
            pattern = re.compile(r"(I!\"'''\")")
            self._score = pattern.sub("I!''", self._score)
            pattern = re.compile(r"(\"'''\"\n!I)")
            self._score = pattern.sub("''!I", self._score)

    def clean_content(self):
        pattern = re.compile(r"(\"'''\"[\n]{0,1})")
        return pattern.sub("", self._score)
