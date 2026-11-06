import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go

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


# -----------------------------------
# RECEIVED POWER VS SLANT RANGE GRAPH
# -----------------------------------

st.divider()

st.header("📈 Received Power vs. Slant Range")

st.write(
    "This graph shows how received signal power "
    "changes with satellite-to-ground distance."
)

max_range = st.number_input(
    "Maximum Slant Range (km)",
    min_value=100.0,
    value=3000.0,
    step=100.0
)

errors = validate_inputs()

if errors:
    st.warning(
        "Please correct the mission inputs "
        "before generating the graph."
    )

elif max_range <= altitude:
    st.warning(
        "Maximum slant range must be greater "
        "than satellite altitude."
    )

else:
    # Generate 100 slant range values
    distances = np.linspace(
        max(altitude, 1.0),
        max_range,
        100
    )

    received_powers = []

    # Calculate received power at each distance
    for distance in distances:

        result = calculate_received_power(
            tx_power_watts=10 ** (tx_power / 10),
            tx_antenna_gain_dbi=tx_gain,
            rx_antenna_gain_dbi=rx_gain,
            frequency_hz=frequency * 1e9,
            slant_range_m=distance * 1000,
            additional_losses_db=system_losses
        )

        received_powers.append(
            result["received_power_dbm"]
        )

    # Create Plotly line graph
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=distances,
            y=received_powers,
            mode="lines",
            name="Received Power",
            line=dict(width=3)
        )
    )

    fig.update_layout(
        title="Received Power vs. Slant Range",
        xaxis_title="Slant Range (km)",
        yaxis_title="Received Power (dBm)",
        hovermode="x unified",
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------------
# LINK BUDGET WATERFALL CHART
# -----------------------------------

st.divider()

st.header("📊 Link Budget Waterfall Chart")

st.write(
    "This chart shows how transmitter power, "
    "antenna gains, and propagation losses "
    "contribute to the final received power."
)

errors = validate_inputs()

if errors:
    st.warning(
        "Please enter valid mission parameters "
        "to generate the waterfall chart."
    )

else:
    try:
        # Calculate using Kevin's backend
        result = calculate_received_power(
            tx_power_watts=10 ** (tx_power / 10),
            tx_antenna_gain_dbi=tx_gain,
            rx_antenna_gain_dbi=rx_gain,
            frequency_hz=frequency * 1e9,
            slant_range_m=slant_range * 1000,
            additional_losses_db=system_losses
        )

        # Convert transmitter power from dBW to dBm
        tx_power_dbm = tx_power + 30

        # Create Plotly waterfall
        waterfall = go.Figure(
            go.Waterfall(
                name="Link Budget",
                orientation="v",
                measure=[
                    "absolute",
                    "relative",
                    "relative",
                    "relative",
                    "relative",
                    "total"
                ],
                x=[
                    "Tx Power",
                    "Tx Gain",
                    "Rx Gain",
                    "FSPL",
                    "Other Losses",
                    "Received Power"
                ],
                y=[
                    tx_power_dbm,
                    tx_gain,
                    rx_gain,
                    -result["fspl_db"],
                    -system_losses,
                    0
                ],
                connector={"line": {"color": "gray"}},
                textposition="outside",
                text=[
                    f"{tx_power_dbm:.2f}",
                    f"+{tx_gain:.2f}",
                    f"+{rx_gain:.2f}",
                    f"-{result['fspl_db']:.2f}",
                    f"-{system_losses:.2f}",
                    f"{result['received_power_dbm']:.2f}"
                ]
            )
        )

        waterfall.update_layout(
            title="Satellite Communication Link Budget",
            xaxis_title="Link Budget Components",
            yaxis_title="Cumulative Power (dBm)",
            template="plotly_white",
            showlegend=False,
            height=550
        )

        st.plotly_chart(
            waterfall,
            use_container_width=True
        )

        # Verify waterfall result
        waterfall_total = (
            tx_power_dbm
            + tx_gain
            + rx_gain
            - result["fspl_db"]
            - system_losses
        )

        difference = abs(
            waterfall_total - result["received_power_dbm"]
        )

        if difference <= 0.02:
            st.success(
                "Waterfall chart matches the "
                "backend received power calculation."
            )
        else:
            st.warning(
                "Waterfall total differs from "
                "the backend calculation."
            )

        st.metric(
            "Final Received Power",
            f"{result['received_power_dbm']:.2f} dBm"
        )

    except (ValueError, OverflowError) as error:
        st.error(f"Waterfall calculation error: {error}")



# -----------------------------------
# MISSION A VS MISSION B COMPARISON
# -----------------------------------

st.divider()
st.header("🛰️ Mission A vs. Mission B Comparison")

st.write(
    "Compare two independent satellite communication "
    "missions using the link budget calculation engine."
)

col_a, col_b = st.columns(2)

# -----------------------------------
# MISSION A INPUTS
# -----------------------------------

with col_a:
    st.subheader("Mission A")

    a_altitude = st.number_input(
        "Altitude A (km)",
        min_value=100.0,
        value=500.0,
        key="a_altitude"
    )

    a_range = st.number_input(
        "Slant Range A (km)",
        min_value=0.0,
        value=500.0,
        key="a_range"
    )

    a_frequency = st.number_input(
        "Frequency A (GHz)",
        min_value=0.0,
        value=2.2,
        key="a_frequency"
    )

    a_power = st.number_input(
        "Tx Power A (dBW)",
        value=20.0,
        key="a_power"
    )

    a_tx_gain = st.number_input(
        "Tx Gain A (dBi)",
        value=15.0,
        key="a_tx_gain"
    )

    a_rx_gain = st.number_input(
        "Rx Gain A (dBi)",
        value=30.0,
        key="a_rx_gain"
    )

    a_losses = st.number_input(
        "System Losses A (dB)",
        min_value=0.0,
        value=2.0,
        key="a_losses"
    )

# -----------------------------------
# MISSION B INPUTS
# -----------------------------------

with col_b:
    st.subheader("Mission B")

    b_altitude = st.number_input(
        "Altitude B (km)",
        min_value=100.0,
        value=800.0,
        key="b_altitude"
    )

    b_range = st.number_input(
        "Slant Range B (km)",
        min_value=0.0,
        value=1000.0,
        key="b_range"
    )

    b_frequency = st.number_input(
        "Frequency B (GHz)",
        min_value=0.0,
        value=5.0,
        key="b_frequency"
    )

    b_power = st.number_input(
        "Tx Power B (dBW)",
        value=25.0,
        key="b_power"
    )

    b_tx_gain = st.number_input(
        "Tx Gain B (dBi)",
        value=20.0,
        key="b_tx_gain"
    )

    b_rx_gain = st.number_input(
        "Rx Gain B (dBi)",
        value=35.0,
        key="b_rx_gain"
    )

    b_losses = st.number_input(
        "System Losses B (dB)",
        min_value=0.0,
        value=3.0,
        key="b_losses"
    )

# -----------------------------------
# VALIDATE AND CALCULATE BOTH MISSIONS
# -----------------------------------

def calculate_mission(altitude, distance, freq, power,
                      tx_gain, rx_gain, losses):

    if not (100 <= altitude <= 50000):
        raise ValueError(
            "Altitude must be between 100 and 50,000 km."
        )

    if distance < altitude:
        raise ValueError(
            "Slant range must be at least the altitude."
        )

    if freq <= 0:
        raise ValueError(
            "Frequency must be greater than zero."
        )

    if losses < 0:
        raise ValueError(
            "System losses cannot be negative."
        )

    return calculate_received_power(
        tx_power_watts=10 ** (power / 10),
        tx_antenna_gain_dbi=tx_gain,
        rx_antenna_gain_dbi=rx_gain,
        frequency_hz=freq * 1e9,
        slant_range_m=distance * 1000,
        additional_losses_db=losses
    )


try:
    result_a = calculate_mission(
        a_altitude, a_range, a_frequency, a_power,
        a_tx_gain, a_rx_gain, a_losses
    )

    result_b = calculate_mission(
        b_altitude, b_range, b_frequency, b_power,
        b_tx_gain, b_rx_gain, b_losses
    )

    # -----------------------------------
    # SIDE-BY-SIDE RESULTS
    # -----------------------------------

    st.divider()
    st.subheader("Mission Comparison Results")

    result_col_a, result_col_b = st.columns(2)

    with result_col_a:
        st.markdown("### Mission A")

        st.metric(
            "FSPL",
            f"{result_a['fspl_db']:.2f} dB"
        )

        st.metric(
            "EIRP",
            f"{result_a['eirp_dbw']:.2f} dBW"
        )

        st.metric(
            "Received Power",
            f"{result_a['received_power_dbm']:.2f} dBm"
        )

    with result_col_b:
        st.markdown("### Mission B")

        st.metric(
            "FSPL",
            f"{result_b['fspl_db']:.2f} dB"
        )

        st.metric(
            "EIRP",
            f"{result_b['eirp_dbw']:.2f} dBW"
        )

        st.metric(
            "Received Power",
            f"{result_b['received_power_dbm']:.2f} dBm"
        )

    # -----------------------------------
    # COMPARISON GRAPH
    # -----------------------------------

    st.subheader("Graphical Comparison")

    comparison_fig = go.Figure()

    comparison_fig.add_trace(
        go.Bar(
            name="Mission A",
            x=["Received Power (dBm)", "FSPL (dB)"],
            y=[
                result_a["received_power_dbm"],
                result_a["fspl_db"]
            ]
        )
    )

    comparison_fig.add_trace(
        go.Bar(
            name="Mission B",
            x=["Received Power (dBm)", "FSPL (dB)"],
            y=[
                result_b["received_power_dbm"],
                result_b["fspl_db"]
            ]
        )
    )

    comparison_fig.update_layout(
        title="Mission A vs. Mission B",
        barmode="group",
        template="plotly_white",
        yaxis_title="Numerical Value"
    )

    st.plotly_chart(
        comparison_fig,
        use_container_width=True
    )

except (ValueError, OverflowError) as error:
    st.error(f"Mission comparison error: {error}")
