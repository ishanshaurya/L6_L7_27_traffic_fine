import pytest
from traffic_fine import speeding_fine, license_action, total_penalty


def test_no_speeding():
    assert speeding_fine(50, 60, "city") == 0


def test_school_zone_over_40():
    assert speeding_fine(110, 60, "school") == 6000


def test_highway_zone_over_20():
    assert speeding_fine(90, 60, "highway") == 2000


def test_city_zone_base_fine():
    assert speeding_fine(70, 60, "city") == 500


def test_commercial_revoked():
    assert license_action(12, True, False) == "revoke"


def test_non_commercial_suspended():
    assert license_action(12, False, False) == "suspend"


def test_repeat_offender_suspended():
    assert license_action(8, False, True) == "suspend"


def test_first_offence_warning():
    assert license_action(8, False, False) == "warning"


def test_notice():
    assert license_action(4, False, False) == "notice"


def test_clean_record():
    assert license_action(2, False, False) == "none"


def test_total_sums_fines():
    assert total_penalty([100, 200]) == 300


def test_negative_fine_rejected():
    with pytest.raises(ValueError):
        total_penalty([100, -1])


def test_total_capped():
    assert total_penalty([6000, 6000]) == 10000
