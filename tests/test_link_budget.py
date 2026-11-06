import pytest
from modules.calculations.link_budget import (
    calculate_fspl,
    calculate_eirp,
    calculate_received_power,
    calculate_thermal_noise,
    calculate_c_n0,
    calculate_eb_n0,
    calculate_link_margin,
    evaluate_link_budget,
    calculate_distance_sensitivity,
    watts_to_dbw,
    watts_to_dbm,
    dbw_to_dbm,
)


def test_unit_conversions():
    assert pytest.approx(watts_to_dbw(10.0), 0.01) == 10.0
    assert pytest.approx(watts_to_dbm(10.0), 0.01) == 40.0
    assert dbw_to_dbm(25.0) == 55.0


def test_invalid_inputs_day1():
    with pytest.raises(ValueError):
        calculate_fspl(-2.2e9, 1000000.0)
    with pytest.raises(ValueError):
        calculate_fspl(2.2e9, 0.0)
    with pytest.raises(ValueError):
        watts_to_dbw(0.0)


def test_link_budget_day1_case():
    results = calculate_received_power(
        tx_power_watts=10.0,
        tx_antenna_gain_dbi=15.0,
        rx_antenna_gain_dbi=35.0,
        frequency_hz=2.2e9,
        slant_range_m=1000000.0,
        additional_losses_db=2.0,
    )
    assert results["eirp_dbw"] == 25.0
    assert pytest.approx(results["fspl_db"], 0.05) == 159.31
    assert pytest.approx(results["received_power_dbm"], 0.05) == -71.31


def test_thermal_noise_calculation():
    noise = calculate_thermal_noise(system_temp_k=290.0, bandwidth_hz=1e6)
    assert pytest.approx(noise["noise_power_watts"], rel=1e-3) == 4.00388e-15
    assert pytest.approx(noise["noise_power_dbm"], 0.05) == -113.98


def test_invalid_inputs_day2():
    with pytest.raises(ValueError):
        calculate_thermal_noise(system_temp_k=-10.0, bandwidth_hz=1e6)
    with pytest.raises(ValueError):
        calculate_thermal_noise(system_temp_k=290.0, bandwidth_hz=0.0)
    with pytest.raises(ValueError):
        calculate_c_n0(received_power_dbw=-100.0, system_temp_k=-5.0)
    with pytest.raises(ValueError):
        calculate_eb_n0(c_n0_db_hz=80.0, bit_rate_bps=0.0)


def test_link_quality_metrics():
    c_n0 = calculate_c_n0(received_power_dbw=-101.31, system_temp_k=290.0)
    assert pytest.approx(c_n0, 0.05) == 102.67

    eb_n0 = calculate_eb_n0(c_n0_db_hz=c_n0, bit_rate_bps=1e6)
    assert pytest.approx(eb_n0, 0.05) == 42.67

    margin = calculate_link_margin(available_eb_n0_db=eb_n0, required_eb_n0_db=10.0)
    assert pytest.approx(margin, 0.05) == 32.67


def test_link_performance_assessment_thresholds():
    res_pass = evaluate_link_budget(
        tx_power_watts=10.0,
        tx_antenna_gain_dbi=15.0,
        rx_antenna_gain_dbi=35.0,
        frequency_hz=2.2e9,
        slant_range_m=1000000.0,
        system_temp_k=290.0,
        bandwidth_hz=1e6,
        bit_rate_bps=1e6,
        required_eb_n0_db=10.0,
        additional_losses_db=2.0,
    )
    assert res_pass["is_link_closed"] is True
    assert "PASS" in res_pass["link_status"]
    assert res_pass["link_margin_db"] > 0

    res_fail = evaluate_link_budget(
        tx_power_watts=10.0,
        tx_antenna_gain_dbi=15.0,
        rx_antenna_gain_dbi=35.0,
        frequency_hz=2.2e9,
        slant_range_m=1000000.0,
        system_temp_k=290.0,
        bandwidth_hz=1e6,
        bit_rate_bps=1e6,
        required_eb_n0_db=50.0,
        additional_losses_db=2.0,
    )
    assert res_fail["is_link_closed"] is False
    assert "FAIL" in res_fail["link_status"]
    assert res_fail["link_margin_db"] < 0


def test_distance_sensitivity_monotonicity():
    sensitivity = calculate_distance_sensitivity(
        tx_power_watts=10.0,
        tx_antenna_gain_dbi=15.0,
        rx_antenna_gain_dbi=35.0,
        frequency_hz=2.2e9,
        system_temp_k=290.0,
        bandwidth_hz=1e6,
        bit_rate_bps=1e6,
        required_eb_n0_db=10.0,
        min_slant_range_m=500_000.0,
        max_slant_range_m=2_000_000.0,
        num_points=10,
        additional_losses_db=2.0,
    )

    powers = sensitivity["received_powers_dbm"]
    margins = sensitivity["link_margins_db"]

    for i in range(len(powers) - 1):
        assert powers[i] > powers[i + 1]
        assert margins[i] > margins[i + 1]
