import streamlit as st
import math

from modules.calculations.link_budget import calculate_received_power

st.set_page_config(
    page_title="SatLink",
    page_icon="🛰️",
    layout="wide"
)

st.title("🛰️ SatLink")

st.subheader(
    "Satellite Communication Link Budget "
    "and Mission Analysis Platform"
)

st.write("Welcome to the SatLink Mission Analysis Dashboard!")

# -----------------------------------
# MISSION CONFIGURATION SIDEBAR
# -----------------------------------

st.sidebar.header("Mission Configuration")

mission_name = st.sidebar.text_input(
    "Mission Name",
    value="SatLink Demo"
)

altitude = st.sidebar.number_input(
    "Satellite Altitude (km)",
    min_value=0.0,
    value=500.0,
    step=10.0
)
# NEW: Satellite Slant Range
slant_range = st.sidebar.number_input(
    "Satellite Slant Range (km)",
    min_value=0.0,
    value=500.0,
    step=10.0,
    help="Distance between the satellite and ground station"
)

frequency = st.sidebar.number_input(
    "Communication Frequency (GHz)",
    min_value=0.0,
    value=2.2,
    step=0.1
)

tx_power = st.sidebar.number_input(
    "Transmitter Power (dBW)",
    value=20.0,
    step=1.0
)

tx_gain = st.sidebar.number_input(
    "Transmitter Antenna Gain (dBi)",
    value=15.0,
    step=1.0
)

rx_gain = st.sidebar.number_input(
    "Receiver Antenna Gain (dBi)",
    value=30.0,
    step=1.0
)

system_losses = st.sidebar.number_input(
    "System Losses (dB)",
    min_value=0.0,
    value=2.0,
    step=0.5
)

data_rate = st.sidebar.number_input(
    "Data Rate (Mbps)",
    min_value=0.0,
    value=1.0,
    step=0.1
)

# -----------------------------------
# INPUT VALIDATION
# -----------------------------------

import math

def validate_inputs():
    errors = []

    # Check mission name
    if not mission_name.strip():
        errors.append("Mission name cannot be empty.")

    # Check satellite altitude
    if not math.isfinite(altitude) or not (100 <= altitude <= 50000):
        errors.append(
            "Satellite altitude must be between "
            "100 and 50,000 km."
        )

    # Check frequency
    if not math.isfinite(frequency) or frequency <= 0:
        errors.append(
            "Frequency must be greater than 0 GHz."
        )

    # Check transmitter power
    if not math.isfinite(tx_power):
        errors.append(
            "Transmitter power must be a finite number."
        )

    # Check antenna gains
    if not math.isfinite(tx_gain) or not math.isfinite(rx_gain):
        errors.append(
            "Antenna gains must be finite numbers."
        )

    # Check system losses
    if not math.isfinite(system_losses) or system_losses < 0:
        errors.append(
            "System losses cannot be negative."
        )

        # Check data rate
    if not math.isfinite(data_rate) or data_rate <= 0:
        errors.append(
            "Data rate must be greater than zero."
        )

    # Check satellite slant range
    if not math.isfinite(slant_range) or slant_range < altitude:
        errors.append(
            "Slant range must be at least the satellite altitude."
        )

    return errors


# -----------------------------------
# VALIDATE MISSION BUTTON
# -----------------------------------

st.divider()

st.header("Mission Validation")

if st.button("Validate Mission Configuration"):

    errors = validate_inputs()

    if errors:
        for error in errors:
            st.error(error)
    else:
        st.success(
            "Mission configuration validated successfully!"
        )

# -----------------------------------
# MISSION SUMMARY
# -----------------------------------

st.divider()
# -----------------------------------
# LINK BUDGET RESULTS DASHBOARD
# -----------------------------------


# -----------------------------------
# LINK BUDGET RESULTS DASHBOARD
# -----------------------------------

st.divider()

st.header("📊 Link Budget Results")

# Store results between Streamlit reruns
if "link_results" not in st.session_state:
    st.session_state.link_results = None

if "last_inputs" not in st.session_state:
    st.session_state.last_inputs = None

current_inputs = (
    mission_name,
    altitude,
    slant_range,
    frequency,
    tx_power,
    tx_gain,
    rx_gain,
    system_losses,
    data_rate
)

# Clear outdated results when inputs change
if st.session_state.last_inputs != current_inputs:
    st.session_state.link_results = None

if st.button("Calculate Link Budget"):

    errors = validate_inputs()

    if errors:
        st.session_state.link_results = None

        for error in errors:
            st.error(error)

    else:
        try:
            # Convert GHz to Hz
            frequency_hz = frequency * 1e9

            # Convert km to metres
            slant_range_m = slant_range * 1000

            # Convert dBW to Watts
            tx_power_watts = 10 ** (tx_power / 10)

            # Call Kevin's calculation engine
            results = calculate_received_power(
                tx_power_watts=tx_power_watts,
                tx_antenna_gain_dbi=tx_gain,
                rx_antenna_gain_dbi=rx_gain,
                frequency_hz=frequency_hz,
                slant_range_m=slant_range_m,
                additional_losses_db=system_losses
            )

            st.session_state.link_results = results
            st.session_state.last_inputs = current_inputs

            st.success(
                "Link budget calculated successfully!"
            )

        except (ValueError, OverflowError) as error:
            st.session_state.link_results = None
            st.error(f"Calculation error: {error}")

# Display results
results = st.session_state.link_results

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Free Space Path Loss (FSPL)",
        f"{results['fspl_db']:.2f} dB"
        if results is not None else "N/A"
    )

with col2:
    st.metric(
        "Received Power",
        f"{results['received_power_dbw']:.2f} dBW"
        if results is not None else "N/A"
    )

with col3:
    st.metric(
        "EIRP",
        f"{results['eirp_dbw']:.2f} dBW"
        if results is not None else "N/A"
    )

if results is None:
    st.info(
        "Enter valid mission parameters and click "
        "Calculate Link Budget to view results."
    )


st.header("🛰️ Mission Summary")

st.write(f"**Mission Name:** {mission_name}")
st.write(f"**Satellite Altitude:** {altitude} km")
st.write(f"**Communication Frequency:** {frequency} GHz")
st.write(f"**Transmitter Power:** {tx_power} dBW")
st.write(f"**Transmitter Antenna Gain:** {tx_gain} dBi")
st.write(f"**Receiver Antenna Gain:** {rx_gain} dBi")
st.write(f"**System Losses:** {system_losses} dB")
st.write(f"**Data Rate:** {data_rate} Mbps")
