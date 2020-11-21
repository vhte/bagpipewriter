import re
from bagpipemanager.embellishments import Embellishments
from bagpipemanager.exceptions import BagpipeManagerException


class Sheet:
    TUNE_TEMPO = "TuneTempo"
    STAFF = r"& sharpf sharpc 4_4"  # TODO space regex + use group to replace in file?

    def __init__(self, score, tempo=0):
        self._header, self._tune = self._separate_header_tune(score)
        self._tempo = tempo
        self._embellishments = Embellishments()

    @property
    def score(self):
        return self._header + "\n" + self.STAFF + self._score

    @score.setter
    def score(self, content):
        self._header, self._tune = self._separate_header_tune(content)

    @property
    def tune(self):
        return self._score

    @tune.setter
    def tune(self, content):
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

    def toggle_embellishments(self, disable):
        embellishments = self._embellishments.get_all()
        for embellishment in embellishments:
            if disable is True:
                pattern = re.compile(embellishment)
                self._score = pattern.sub("\"{}\"".format(embellishment), self._score)
            else:
                pattern = re.compile("\"{}\"".format(embellishment))
                self._score = pattern.sub(embellishment, self._score)

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

    def _separate_header_tune(self, content):
        """Divides the sheet content into header and tune"""
        try:
            self._header, self._score = content.split(self.STAFF)
        except ValueError as ve:
            raise BagpipeManagerException(r"None or more than one staff signature ({}) found in .bww file: {}".format(self.STAFF, str(ve)))

        return self._header, self._score