"""
SatLink Satellite Communication Link Budget Calculation Engine.
Description: Reusable backend module for calculating Free Space Path Loss (FSPL),
EIRP, Received Signal Power, and unit conversions.
"""

import math

SPEED_OF_LIGHT = 299792458.0  # m/s


def watts_to_dbw(power_watts: float) -> float:
    """Convert power in Watts to dBW."""
    if power_watts <= 0:
        raise ValueError("Power must be greater than zero.")
    return 10.0 * math.log10(power_watts)


def watts_to_dbm(power_watts: float) -> float:
    """Convert power in Watts to dBm."""
    if power_watts <= 0:
        raise ValueError("Power must be greater than zero.")
    return 10.0 * math.log10(power_watts * 1000.0)


def dbw_to_dbm(power_dbw: float) -> float:
    """Convert power in dBW to dBm."""
    return power_dbw + 30.0


def dbm_to_dbw(power_dbm: float) -> float:
    """Convert power in dBm to dBW."""
    return power_dbm - 30.0


def calculate_fspl(frequency_hz: float, slant_range_m: float) -> float:
    """Calculate Free Space Path Loss (FSPL) in dB."""
    if frequency_hz <= 0 or slant_range_m <= 0:
        raise ValueError("Frequency and slant range must be positive non-zero values.")
    ratio = (4.0 * math.pi * slant_range_m * frequency_hz) / SPEED_OF_LIGHT
    return 20.0 * math.log10(ratio)


def calculate_eirp(tx_power_watts: float, tx_antenna_gain_dbi: float) -> float:
    """Calculate Effective Isotropic Radiated Power (EIRP) in dBW."""
    pt_dbw = watts_to_dbw(tx_power_watts)
    return pt_dbw + tx_antenna_gain_dbi


def calculate_received_power(
    tx_power_watts: float,
    tx_antenna_gain_dbi: float,
    rx_antenna_gain_dbi: float,
    frequency_hz: float,
    slant_range_m: float,
    additional_losses_db: float = 0.0,
) -> dict:
    """Calculate Received Signal Power and link budget parameters."""
    if additional_losses_db < 0:
        raise ValueError("Additional losses cannot be negative.")

    eirp_dbw = calculate_eirp(tx_power_watts, tx_antenna_gain_dbi)
    fspl_db = calculate_fspl(frequency_hz, slant_range_m)
    total_losses_db = fspl_db + additional_losses_db

    pr_dbw = eirp_dbw + rx_antenna_gain_dbi - total_losses_db
    pr_dbm = dbw_to_dbm(pr_dbw)

    return {
        "eirp_dbw": round(eirp_dbw, 2),
        "fspl_db": round(fspl_db, 2),
        "total_losses_db": round(total_losses_db, 2),
        "received_power_dbw": round(pr_dbw, 2),
        "received_power_dbm": round(pr_dbm, 2),
    }
