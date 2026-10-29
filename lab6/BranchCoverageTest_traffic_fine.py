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


# Boundaries: each comparison checked on both sides of its threshold
def test_speed_equal_to_limit_is_free():
    assert speeding_fine(60, 60, "city") == 0


def test_one_over_limit():
    assert speeding_fine(61, 60, "city") == 500


def test_excess_exactly_20_is_base_fine():
    assert speeding_fine(80, 60, "city") == 500


def test_excess_21_is_double():
    assert speeding_fine(81, 60, "city") == 1000


def test_excess_exactly_40_is_double():
    assert speeding_fine(100, 60, "city") == 1000


def test_excess_41_is_triple():
    assert speeding_fine(101, 60, "city") == 1500


def test_unknown_zone_uses_base():
    assert speeding_fine(70, 60, "village") == 500


def test_points_11_below_suspend_threshold():
    assert license_action(11, True, False) == "warning"


def test_points_7_below_warning_threshold():
    assert license_action(7, False, True) == "notice"


def test_points_3_below_notice_threshold():
    assert license_action(3, False, False) == "none"


def test_commercial_flag_ignored_below_12():
    assert license_action(8, True, True) == "suspend"


def test_empty_fines():
    assert total_penalty([]) == 0


def test_total_exactly_10000_not_capped():
    assert total_penalty([5000, 5000]) == 10000


def test_total_10001_capped():
    assert total_penalty([10001]) == 10000


def test_zero_fine_allowed():
    assert total_penalty([0]) == 0
