"""
SatLink Satellite Communication Link Budget & Quality Engine.
Modules: calculations/link_budget.py
Covers:
- Day 1: FSPL, EIRP, Received Signal Power, Unit Conversions
- Day 2: Thermal Noise (kTB), C/N0, Eb/N0, Link Margin
- Day 3: Integrated Link Assessment & Slant Distance Sensitivity
"""

import math
from typing import Dict, List, Any

# Fundamental physical constants
SPEED_OF_LIGHT = 299792458.0  # m/s
BOLTZMANN_CONSTANT = 1.380649e-23  # J/K (W/(Hz*K))


def watts_to_dbw(power_watts: float) -> float:
    """Convert power in Watts to dBW."""
    if power_watts <= 0:
        raise ValueError("Power must be strictly positive.")
    return 10.0 * math.log10(power_watts)


def watts_to_dbm(power_watts: float) -> float:
    """Convert power in Watts to dBm."""
    if power_watts <= 0:
        raise ValueError("Power must be strictly positive.")
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
    return watts_to_dbw(tx_power_watts) + tx_antenna_gain_dbi


def calculate_received_power(
    tx_power_watts: float,
    tx_antenna_gain_dbi: float,
    rx_antenna_gain_dbi: float,
    frequency_hz: float,
    slant_range_m: float,
    additional_losses_db: float = 0.0,
) -> Dict[str, float]:
    """Calculate received carrier power and basic link metrics."""
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


def calculate_thermal_noise(system_temp_k: float, bandwidth_hz: float) -> Dict[str, float]:
    """Calculate thermal noise power N = kTB."""
    if system_temp_k <= 0 or bandwidth_hz <= 0:
        raise ValueError("System noise temperature and bandwidth must be strictly positive.")

    noise_watts = BOLTZMANN_CONSTANT * system_temp_k * bandwidth_hz
    noise_dbw = watts_to_dbw(noise_watts)
    noise_dbm = dbw_to_dbm(noise_dbw)
    n0_dbw_hz = 10.0 * math.log10(BOLTZMANN_CONSTANT * system_temp_k)

    return {
        "noise_power_watts": noise_watts,
        "noise_power_dbm": round(noise_dbm, 2),
        "noise_power_dbw": round(noise_dbw, 2),
        "n0_dbw_hz": round(n0_dbw_hz, 2),
    }


def calculate_c_n0(received_power_dbw: float, system_temp_k: float) -> float:
    """Calculate Carrier-to-Noise Density Ratio (C/N0) in dB-Hz."""
    if system_temp_k <= 0:
        raise ValueError("System noise temperature must be positive non-zero.")
    n0_dbw = 10.0 * math.log10(BOLTZMANN_CONSTANT * system_temp_k)
    return received_power_dbw - n0_dbw


def calculate_eb_n0(c_n0_db_hz: float, bit_rate_bps: float) -> float:
    """Calculate Energy per Bit to Noise Density Ratio (Eb/N0) in dB."""
    if bit_rate_bps <= 0:
        raise ValueError("Bit rate must be strictly positive.")
    return c_n0_db_hz - (10.0 * math.log10(bit_rate_bps))


def calculate_link_margin(available_eb_n0_db: float, required_eb_n0_db: float) -> float:
    """Calculate Link Margin in dB (Available Eb/N0 - Required Eb/N0)."""
    return available_eb_n0_db - required_eb_n0_db


def evaluate_link_budget(
    tx_power_watts: float,
    tx_antenna_gain_dbi: float,
    rx_antenna_gain_dbi: float,
    frequency_hz: float,
    slant_range_m: float,
    system_temp_k: float,
    bandwidth_hz: float,
    bit_rate_bps: float,
    required_eb_n0_db: float,
    additional_losses_db: float = 0.0,
) -> Dict[str, Any]:
    """Execute complete end-to-end satellite link performance assessment."""
    rx_summary = calculate_received_power(
        tx_power_watts=tx_power_watts,
        tx_antenna_gain_dbi=tx_antenna_gain_dbi,
        rx_antenna_gain_dbi=rx_antenna_gain_dbi,
        frequency_hz=frequency_hz,
        slant_range_m=slant_range_m,
        additional_losses_db=additional_losses_db,
    )

    noise_summary = calculate_thermal_noise(
        system_temp_k=system_temp_k,
        bandwidth_hz=bandwidth_hz,
    )

    c_n0 = calculate_c_n0(rx_summary["received_power_dbw"], system_temp_k)
    eb_n0 = calculate_eb_n0(c_n0, bit_rate_bps)
    margin = calculate_link_margin(eb_n0, required_eb_n0_db)

    is_link_closed = margin >= 0.0
    status = "LINK CLOSED (PASS)" if is_link_closed else "LINK DEGRADED (FAIL)"

    return {
        "eirp_dbw": rx_summary["eirp_dbw"],
        "fspl_db": rx_summary["fspl_db"],
        "received_power_dbw": rx_summary["received_power_dbw"],
        "received_power_dbm": rx_summary["received_power_dbm"],
        "noise_power_dbm": noise_summary["noise_power_dbm"],
        "c_n0_db_hz": round(c_n0, 2),
        "eb_n0_db": round(eb_n0, 2),
        "required_eb_n0_db": round(required_eb_n0_db, 2),
        "link_margin_db": round(margin, 2),
        "is_link_closed": is_link_closed,
        "link_status": status,
    }


def calculate_distance_sensitivity(
    tx_power_watts: float,
    tx_antenna_gain_dbi: float,
    rx_antenna_gain_dbi: float,
    frequency_hz: float,
    system_temp_k: float,
    bandwidth_hz: float,
    bit_rate_bps: float,
    required_eb_n0_db: float,
    min_slant_range_m: float,
    max_slant_range_m: float,
    num_points: int = 50,
    additional_losses_db: float = 0.0,
) -> Dict[str, List[float]]:
    """Evaluate received power and link margin across a range of slant distances."""
    if min_slant_range_m <= 0 or max_slant_range_m <= min_slant_range_m:
        raise ValueError("Invalid slant range bounds. Must be positive and max > min.")
    if num_points < 2:
        raise ValueError("num_points must be at least 2.")

    step = (max_slant_range_m - min_slant_range_m) / (num_points - 1)
    ranges_km: List[float] = []
    received_powers_dbm: List[float] = []
    link_margins_db: List[float] = []

    for i in range(num_points):
        d_m = min_slant_range_m + (i * step)
        res = evaluate_link_budget(
            tx_power_watts=tx_power_watts,
            tx_antenna_gain_dbi=tx_antenna_gain_dbi,
            rx_antenna_gain_dbi=rx_antenna_gain_dbi,
            frequency_hz=frequency_hz,
            slant_range_m=d_m,
            system_temp_k=system_temp_k,
            bandwidth_hz=bandwidth_hz,
            bit_rate_bps=bit_rate_bps,
            required_eb_n0_db=required_eb_n0_db,
            additional_losses_db=additional_losses_db,
        )
        ranges_km.append(round(d_m / 1000.0, 2))
        received_powers_dbm.append(res["received_power_dbm"])
        link_margins_db.append(res["link_margin_db"])

    return {
        "slant_ranges_km": ranges_km,
        "received_powers_dbm": received_powers_dbm,
        "link_margins_db": link_margins_db,
    }
