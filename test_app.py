from app import check_levels


def test_fires_once_then_rearms():
    fired = set()
    assert len(check_levels(2410, 2400, None, fired)) == 1
    assert check_levels(2415, 2400, None, fired) == []
    assert check_levels(2390, 2400, None, fired) == []
    assert len(check_levels(2405, 2400, None, fired)) == 1


def test_below_level():
    assert len(check_levels(2290, None, 2300, set())) == 1
