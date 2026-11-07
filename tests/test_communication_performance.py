
import math
import pytest

from modules.calculations.link_budget import (
    calculate_thermal_noise,
    calculate_c_n0,
    calculate_eb_n0,
    calculate_link_margin,
    evaluate_link_budget,
    calculate_distance_sensitivity,
)


def test_thermal_noise():
    result = calculate_thermal_noise(
        system_temp_k=290,
        bandwidth_hz=1e6
    )

    expected_watts = 1.380649e-23 * 290 * 1e6
    expected_dbm = 10 * math.log10(expected_watts * 1000)

    assert result["noise_power_dbm"] == pytest.approx(
        expected_dbm, abs=0.01
    )


def test_c_n0():
    received_power_dbw = -90
    temperature = 290

    expected = received_power_dbw - 10 * math.log10(
        1.380649e-23 * temperature
    )

    assert calculate_c_n0(
        received_power_dbw, temperature
    ) == pytest.approx(expected)


def test_eb_n0():
    assert calculate_eb_n0(
        80, 1e6
    ) == pytest.approx(20)


def test_positive_link_margin():
    assert calculate_link_margin(15, 10) == 5


def test_negative_link_margin():
    assert calculate_link_margin(5, 10) == -5


def test_link_budget_status():
    params = dict(
        tx_power_watts=100,
        tx_antenna_gain_dbi=15,
        rx_antenna_gain_dbi=30,
        frequency_hz=2.2e9,
        slant_range_m=500e3,
        system_temp_k=290,
        bandwidth_hz=1e6,
        bit_rate_bps=1e6,
        required_eb_n0_db=10,
        additional_losses_db=2
    )

    result = evaluate_link_budget(**params)

    assert result["link_margin_db"] > 0
    assert result["is_link_closed"] is True


def test_margin_decreases_with_distance():
    result = calculate_distance_sensitivity(
        tx_power_watts=100,
        tx_antenna_gain_dbi=15,
        rx_antenna_gain_dbi=30,
        frequency_hz=2.2e9,
        system_temp_k=290,
        bandwidth_hz=1e6,
        bit_rate_bps=1e6,
        required_eb_n0_db=10,
        min_slant_range_m=500e3,
        max_slant_range_m=3000e3,
        num_points=20,
        additional_losses_db=2
    )

    margins = result["link_margins_db"]

    assert len(margins) == 20
    assert margins[0] > margins[-1]


def test_invalid_noise_temperature():
    with pytest.raises(ValueError):
        calculate_thermal_noise(0, 1e6)


def test_invalid_bit_rate():
    with pytest.raises(ValueError):
        calculate_eb_n0(80, 0)
