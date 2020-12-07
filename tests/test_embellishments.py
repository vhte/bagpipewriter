from bagpipemanager.embellishments import Embellishments


def test_get_all():
    embellishments = Embellishments()
    all_embellishments = embellishments.get_all()

    assert len(all_embellishments) == 9
