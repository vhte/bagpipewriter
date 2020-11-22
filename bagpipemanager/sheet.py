import re
from bagpipemanager.embellishments import Embellishments
from bagpipemanager.exceptions import BagpipeManagerException


class Sheet:
    TUNE_TEMPO = "TuneTempo"
    STAFF = r"& sharpf sharpc 4_4"  # TODO space regex + use group to replace in file?

    def __init__(self, file_content, tempo=0):
        self._header, self._score = self._separate_header_tune(file_content)
        self._tempo = tempo
        self._embellishments = Embellishments()

    @property
    def score(self):
        return self._header + self.STAFF + self._score

    @score.setter
    def score(self, content):
        self._header, self._score = self._separate_header_tune(content)

    @property
    def tempo(self):
        tempo = re.findall(r"TuneTempo[\s]*,[\s]*(?P<tempo>[\d]+)", self._header)
        if tempo:
            return int(tempo[0])
        raise ValueError("Couldn't find {} in loaded score.".format(self.TUNE_TEMPO))

    @tempo.setter
    def tempo(self, value):
        pattern = re.compile(r"TuneTempo[\s]*,[\s]*[\d]+")
        self._header = pattern.sub("TuneTempo,{}".format(value), self._header)

    def toggle_embellishments(self, disable):
        embellishments = self._embellishments.get_all()
        for embellishment in embellishments:
            if disable is True:
                self._score = re.sub(embellishment, r'"\1"', self._score)
            else:
                self._score = re.sub(
                    '"{}"'.format(embellishment), r"\1".replace('"', ""), self._score
                )

    def toggle_repetition(self, disable):
        # TODO improve sub() use like toggle_embellishments()
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
            header, score = content.split(self.STAFF)
        except ValueError as ve:
            raise BagpipeManagerException(
                r"None or more than one staff signature ({}) found in .bww file: {}".format(
                    self.STAFF, str(ve)
                )
            )

        return header, score
