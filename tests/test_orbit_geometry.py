
import math
import pytest

from modules.calculations.orbit_geometry import (
    calculate_slant_range,
    EARTH_RADIUS_KM,
)


def test_zenith_range():
    assert calculate_slant_range(
        500, 0
    ) == pytest.approx(500, abs=1e-6)


def test_horizon_range():
    R = EARTH_RADIUS_KM
    h = 500

    horizon_angle = math.degrees(
        math.acos(R / (R + h))
    )

    expected = math.sqrt(h * (2 * R + h))

    assert calculate_slant_range(
        h, horizon_angle
    ) == pytest.approx(expected, abs=1e-6)


def test_range_increases_with_separation():
    assert calculate_slant_range(
        500, 10
    ) > calculate_slant_range(500, 0)


def test_negative_altitude():
    with pytest.raises(ValueError):
        calculate_slant_range(-500, 10)


def test_invalid_separation_angle():
    with pytest.raises(ValueError):
        calculate_slant_range(500, 190)
