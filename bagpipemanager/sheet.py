import re
from bagpipemanager.embellishments import Embellishments
from bagpipemanager.exceptions import BagpipeManagerException
from bagpipemanager.notes import Notes


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
        if disable is True:
            self._score = re.sub(r"(I!'')", "I!\"'''\"", self._score)
            self._score = re.sub(r"(''!I)", "\"'''\"\n!I", self._score)
        else:
            self._score = re.sub(r"(I!\"'''\")", "I!''", self._score)
            self._score = re.sub(r"(\"'''\"\n!I)", "''!I", self._score)

    def jump_notes(self, going_up):
        notes = Notes()
        all_notes = notes.get_all()
        if going_up:
            if re.search(notes.HIGH_A + r"[r,l]?_[0-9]{0,2}", self._score):
                raise BagpipeManagerException("HighA already reached in the tune.")

            sequent = None
            all_notes.reverse()
            for note in all_notes:
                if sequent:
                    self._score = re.sub(
                        note + r"([r,l]?_[0-9]{0,2})", sequent + r"\1", self._score
                    )
                sequent = note
        else:
            if re.search(notes.LOW_G + r"[r,l]?_[0-9]{0,2}", self._score):
                raise BagpipeManagerException("LowG already reached in the tune.")

            precedent = None
            for note in all_notes:
                if precedent:
                    self._score = re.sub(
                        note + r"([r,l]?_[0-9]{0,2})", precedent + r"\1", self._score
                    )
                precedent = note

    def clean_content(self):
        pattern = re.compile(r"(\"'''\"[\n]?)")
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
