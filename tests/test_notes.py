from bagpipemanager.notes import Notes


def test_all_notes():
    notes = Notes()
    all_notes = notes.get_all()

    assert len(all_notes) == 9
