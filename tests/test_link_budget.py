import pytest
from modules.calculations.link_budget import (
    calculate_fspl,
    calculate_eirp,
    calculate_received_power,
    watts_to_dbw,
    watts_to_dbm,
    dbw_to_dbm,
)


def test_unit_conversions():
    assert pytest.approx(watts_to_dbw(10.0), 0.01) == 10.0
    assert pytest.approx(watts_to_dbm(10.0), 0.01) == 40.0
    assert dbw_to_dbm(25.0) == 55.0


def test_invalid_inputs():
    with pytest.raises(ValueError):
        calculate_fspl(-2.2e9, 1000000.0)
    with pytest.raises(ValueError):
        calculate_fspl(2.2e9, 0.0)
    with pytest.raises(ValueError):
        watts_to_dbw(0.0)


def test_link_budget_validation_case():
    freq = 2.2e9
    slant_range = 1000000.0
    pt = 10.0
    gt = 15.0
    gr = 35.0
    losses = 2.0

    results = calculate_received_power(
        tx_power_watts=pt,
        tx_antenna_gain_dbi=gt,
        rx_antenna_gain_dbi=gr,
        frequency_hz=freq,
        slant_range_m=slant_range,
        additional_losses_db=losses,
    )

    assert results["eirp_dbw"] == 25.0
    assert pytest.approx(results["fspl_db"], 0.05) == 159.31
    assert pytest.approx(results["received_power_dbm"], 0.05) == -71.31
