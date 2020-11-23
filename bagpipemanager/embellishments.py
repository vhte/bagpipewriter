class Embellishments:
    GRACE_NOTES = r"([a-g,t]{1}g)"
    DOUBLINGS = r"([a-z]{0,1}db[a-z]{1,2})"
    GRACE_NOTES_STRIKES_STRIKES = r"([a-z]{0,2}st[a-z]{1,3})"
    PELES = r"([a-z]{0,2}pel[a-z]{1,2})"
    BIRLS = r"([a-z]{0,1}br[a-z]{0,1})"
    D_THROWS = r"([a-z]{0,2}thrd)"
    GRIPS = r"([a-z]{0,1}grp[a-z]{0,2})"
    TAORLUATHS = r"(tar[a-z]{0,1})"
    BUBBLYS = r"([a-z]{0,1}bubly)"
    # ACCIDENTALS_NATURAL = r"(natural[a-z]{1,2})"
    # ACCIDENTALS_SHARP = r"(sharp[a-z]{1,2})"

    def __init__(self):
        pass

    def get_all(self):
        return [
            self.GRACE_NOTES,
            self.DOUBLINGS,
            self.GRACE_NOTES_STRIKES_STRIKES,
            self.PELES,
            self.BIRLS,
            self.D_THROWS,
            self.GRIPS,
            self.TAORLUATHS,
            self.BUBBLYS,
        ]
