import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go

from modules.calculations.link_budget import (calculate_received_power, calculate_fspl)
from modules.calculations.orbit_geometry import (
    calculate_slant_range,
    EARTH_RADIUS_KM
)

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
# DASHBOARD NAVIGATION
# -----------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "🛰️ Mission Configuration",
    "📊 Link Budget Analysis",
    "⚖️ Mission Comparison",
    "🌍 Orbit & Ground Station"
])
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
    if not math.isfinite(frequency) or not (0 < frequency <= 1000):
        errors.append(
            "Frequency must be greater than 0 and at most 1000 GHz."
        )

    # Check transmitter power
    if not math.isfinite(tx_power) or not (-300 <= tx_power <= 300):
        errors.append(
            "Transmitter power must be between -300 and 300 dBW."
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
with tab1:
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
# MISSION SUMMARY (TAB 1)
# -----------------------------------
with tab1:
    st.divider()
    st.header("🛰️ Mission Summary")
    st.write(f"**Mission Name:** {mission_name}")
    st.write(f"**Satellite Altitude:** {altitude} km")
    st.write(f"**Satellite Slant Range:** {slant_range} km")
    st.write(f"**Communication Frequency:** {frequency} GHz")
    st.write(f"**Transmitter Power:** {tx_power} dBW")
    st.write(f"**Transmitter Antenna Gain:** {tx_gain} dBi")
    st.write(f"**Receiver Antenna Gain:** {rx_gain} dBi")
    st.write(f"**System Losses:** {system_losses} dB")
    st.write(f"**Data Rate:** {data_rate} Mbps")


# -----------------------------------
# LINK BUDGET ANALYSIS (TAB 2)
# -----------------------------------
with tab2:
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


    # --------------------------------------
    # FREQUENCY SENSITIVITY ANALYSIS
    # --------------------------------------

    st.divider()
    st.header("📡 Frequency Sensitivity Analysis")

    st.write(
        "Analyze how free-space path loss changes "
        "with frequency at a fixed satellite slant range."
    )

    freq_min = st.number_input(
        "Minimum Frequency (GHz)",
        min_value=0.001,
        value=1.0,
        step=0.5,
        key="freq_min"
    )

    freq_max = st.number_input(
        "Maximum Frequency (GHz)",
        min_value=0.001,
        value=10.0,
        step=0.5,
        key="freq_max"
    )

    if freq_min >= freq_max:
        st.error(
            "Maximum frequency must be greater "
            "than minimum frequency."
        )

    elif not math.isfinite(slant_range) or slant_range <= 0:
        st.error("Slant range must be greater than zero.")

    else:
        frequencies = np.linspace(
            freq_min,
            freq_max,
            100
        )

        fspl_values = [
            calculate_fspl(
                frequency_hz=float(f) * 1e9,
                slant_range_m=slant_range * 1000
            )
            for f in frequencies
        ]

        fig_frequency = go.Figure()

        fig_frequency.add_trace(
            go.Scatter(
                x=frequencies,
                y=fspl_values,
                mode="lines",
                name="FSPL"
            )
        )

        # Current operating point
        if math.isfinite(frequency) and frequency > 0:
            current_fspl = calculate_fspl(
                frequency_hz=frequency * 1e9,
                slant_range_m=slant_range * 1000
            )

            fig_frequency.add_trace(
                go.Scatter(
                    x=[frequency],
                    y=[current_fspl],
                    mode="markers",
                    marker=dict(size=12),
                    name="Current Operating Point"
                )
            )

        fig_frequency.update_layout(
            title="FSPL vs. Frequency",
            xaxis_title="Frequency (GHz)",
            yaxis_title="Free Space Path Loss (dB)",
            template="plotly_white",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig_frequency,
            use_container_width=True
        )

        if not (freq_min <= frequency <= freq_max):
            st.info(
                "The current operating frequency is outside "
                "the selected graph range."
            )


    # --------------------------------------
    # COMMUNICATION PERFORMANCE METRICS
    # --------------------------------------

    st.divider()

    st.header("📡 Communication Performance Metrics")

    st.write(
        "Receiver noise and link quality metrics "
        "will be calculated using the communication "
        "performance backend."
    )

    noise_col, cn0_col = st.columns(2)
    ebn0_col, margin_col = st.columns(2)

    with noise_col:
        st.metric(
            "Thermal Noise Power",
            "N/A",
            help="Receiver thermal noise power in dBm."
        )

    with cn0_col:
        st.metric(
            "Carrier-to-Noise Density (C/N₀)",
            "N/A",
            help="Carrier power relative to noise spectral density."
        )

    with ebn0_col:
        st.metric(
            "Energy per Bit to Noise Density (Eb/N₀)",
            "N/A",
            help="Signal energy per bit relative to noise density."
        )

    with margin_col:
        st.metric(
            "Link Margin",
            "N/A",
            help="Available Eb/N₀ minus required Eb/N₀."
        )

    st.info(
        "Communication performance calculations are "
        "awaiting backend integration."
    )

    # --------------------------------------
    # LINK STATUS INDICATOR
    # --------------------------------------

    st.divider()

    st.header("📶 Link Status")

    # Replace None with the actual calculated margin
    # when Kevin's backend is integrated.
    link_margin_db = None

    if link_margin_db is None:
        st.info(
            "LINK STATUS UNAVAILABLE — "
            "Link margin calculation is pending."
        )

    elif link_margin_db >= 0:
        st.success(
            "LINK AVAILABLE — "
            "Theoretical link margin is non-negative."
        )

    else:
        st.error(
            "LINK BELOW THRESHOLD — "
            "Theoretical link margin is negative."
        )

    st.caption(
        "This is a simplified theoretical link assessment, "
        "not a guarantee of real-world communication availability."
    )

    # --------------------------------------
    # LINK MARGIN VS DISTANCE
    # --------------------------------------

    st.divider()

    st.header("📉 Link Margin vs. Slant Range")

    st.write(
        "This graph will show how communication "
        "link margin changes with satellite distance."
    )

    st.info(
        "Link margin graph awaiting backend integration. "
        "No calculated margin values are available yet."
    )

    st.caption(
        "The completed graph will include a horizontal "
        "0 dB threshold separating positive and negative margins."
    )

# ==========================================
# TAB 3 - MISSION COMPARISON
# ==========================================

with tab3:

    st.header("⚖️ Mission A vs. Mission B Comparison")

    st.write(
        "Compare two satellite communication missions "
        "using independent mission parameters."
    )

    col_a, col_b = st.columns(2)

    # --------------------------------------
    # MISSION A INPUTS
    # --------------------------------------

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

    # --------------------------------------
    # MISSION B INPUTS
    # --------------------------------------

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

    # --------------------------------------
    # CALCULATE BOTH MISSIONS
    # --------------------------------------

    try:
        for name, alt, distance, freq, power, gain_tx, gain_rx, losses in [
            ("Mission A", a_altitude, a_range, a_frequency, a_power, a_tx_gain, a_rx_gain, a_losses),
            ("Mission B", b_altitude, b_range, b_frequency, b_power, b_tx_gain, b_rx_gain, b_losses),
        ]:
            values = (alt, distance, freq, power, gain_tx, gain_rx, losses)
            if not all(math.isfinite(v) for v in values):
                raise ValueError(f"{name}: inputs must be finite numbers.")
            if not 100 <= alt <= 50000:
                raise ValueError(f"{name}: altitude must be 100–50,000 km.")
            if distance < alt:
                raise ValueError(f"{name}: slant range must be at least altitude.")
            if not (0 < freq <= 1000) or losses < 0 or not (-300 <= power <= 300):
                raise ValueError(f"{name}: check frequency (0–1000 GHz), power (-300–300 dBW), and nonnegative losses.")
            power_watts = 10 ** (power / 10)
            if not math.isfinite(power_watts) or power_watts <= 0:
                raise ValueError(f"{name}: transmitter power is outside the supported range.")

        result_a = calculate_received_power(
            tx_power_watts=10 ** (a_power / 10),
            tx_antenna_gain_dbi=a_tx_gain,
            rx_antenna_gain_dbi=a_rx_gain,
            frequency_hz=a_frequency * 1e9,
            slant_range_m=a_range * 1000,
            additional_losses_db=a_losses
        )

        result_b = calculate_received_power(
            tx_power_watts=10 ** (b_power / 10),
            tx_antenna_gain_dbi=b_tx_gain,
            rx_antenna_gain_dbi=b_rx_gain,
            frequency_hz=b_frequency * 1e9,
            slant_range_m=b_range * 1000,
            additional_losses_db=b_losses
        )


        # ----------------------------------
        # SIDE-BY-SIDE RESULTS
        # ----------------------------------

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

        # ----------------------------------
        # RECEIVED POWER COMPARISON GRAPH
        # ----------------------------------

        st.divider()

        st.subheader("Received Power Comparison")

        power_fig = go.Figure()

        power_fig.add_trace(
            go.Bar(
                x=["Mission A", "Mission B"],
                y=[
                    result_a["received_power_dbm"],
                    result_b["received_power_dbm"]
                ],
                text=[
                    f"{result_a['received_power_dbm']:.2f}",
                    f"{result_b['received_power_dbm']:.2f}"
                ],
                textposition="auto"
            )
        )

        power_fig.update_layout(
            title="Received Power Comparison",
            xaxis_title="Mission",
            yaxis_title="Received Power (dBm)",
            template="plotly_white"
        )

        st.plotly_chart(
            power_fig,
            use_container_width=True
        )

        # ----------------------------------
        # FSPL COMPARISON GRAPH
        # ----------------------------------

        st.subheader("Free Space Path Loss Comparison")

        fspl_fig = go.Figure()

        fspl_fig.add_trace(
            go.Bar(
                x=["Mission A", "Mission B"],
                y=[
                    result_a["fspl_db"],
                    result_b["fspl_db"]
                ],
                text=[
                    f"{result_a['fspl_db']:.2f}",
                    f"{result_b['fspl_db']:.2f}"
                ],
                textposition="auto"
            )
        )

        fspl_fig.update_layout(
            title="FSPL Comparison",
            xaxis_title="Mission",
            yaxis_title="Free Space Path Loss (dB)",
            template="plotly_white"
        )

        st.plotly_chart(
            fspl_fig,
            use_container_width=True
        )

    except (ValueError, OverflowError) as error:

        st.error(
            f"Mission comparison error: {error}"
        )


# ==========================================
# TAB 4 - ORBIT AND GROUND STATION
# ==========================================

with tab4:

    st.header("🛰️ Satellite Orbit Configuration")

    orbit_type = st.selectbox(
        "Orbit Type",
        ["LEO", "MEO", "GEO"]
    )

    orbit_altitude = st.number_input(
        "Satellite Orbit Altitude (km)",
        min_value=0.0,
        value=500.0,
        step=10.0,
        key="orbit_altitude"
    )

    inclination = st.number_input(
        "Orbital Inclination (degrees)",
        min_value=0.0,
        max_value=180.0,
        value=45.0,
        step=1.0
    )

    eccentricity = st.number_input(
        "Orbital Eccentricity",
        min_value=0.0,
        max_value=0.999999,
        value=0.0,
        step=0.01,
        format="%.4f"
    )

    orbit_errors = []

    if orbit_altitude <= 0:
        orbit_errors.append(
            "Satellite altitude must be greater than zero."
        )

    if orbit_type == "LEO" and not (160 <= orbit_altitude < 2000):
        orbit_errors.append(
            "LEO altitude should be approximately 160–2000 km."
        )

    elif orbit_type == "MEO" and not (2000 <= orbit_altitude < 35786):
        orbit_errors.append(
            "MEO altitude should be approximately 2000–35786 km."
        )

    elif orbit_type == "GEO":
        if abs(orbit_altitude - 35786) > 100:
            orbit_errors.append(
                "GEO altitude should be approximately 35,786 km."
            )

        if abs(inclination) > 0.1 or eccentricity > 0.001:
            orbit_errors.append(
                "An ideal GEO orbit requires near-zero "
                "inclination and eccentricity."
            )

    if orbit_errors:
        for error in orbit_errors:
            st.warning(error)
    else:
        st.success("Orbit configuration validated successfully!")


    # ==========================================
    # GROUND STATION CONFIGURATION
    # ==========================================

    st.divider()

    st.header("📡 Ground Station Configuration")

    ground_station_name = st.text_input(
        "Ground Station Name",
        value="SatLink Ground Station",
        key="ground_station_name"
    )

    latitude = st.number_input(
        "Ground Station Latitude (degrees)",
        min_value=-90.0,
        max_value=90.0,
        value=13.35,
        step=0.01,
        key="ground_latitude"
    )

    longitude = st.number_input(
        "Ground Station Longitude (degrees)",
        min_value=-180.0,
        max_value=180.0,
        value=74.79,
        step=0.01,
        key="ground_longitude"
    )

    min_elevation = st.number_input(
        "Minimum Elevation Angle (degrees)",
        min_value=0.0,
        max_value=90.0,
        value=10.0,
        step=1.0,
        key="minimum_elevation"
    )

    # --------------------------------------
    # GROUND STATION VALIDATION
    # --------------------------------------

    station_errors = []

    if not ground_station_name.strip():
        station_errors.append(
            "Ground station name cannot be empty."
        )

    if not (-90 <= latitude <= 90):
        station_errors.append(
            "Latitude must be between -90 and 90 degrees."
        )

    if not (-180 <= longitude <= 180):
        station_errors.append(
            "Longitude must be between -180 and 180 degrees."
        )

    if not (0 <= min_elevation <= 90):
        station_errors.append(
            "Minimum elevation must be between 0 and 90 degrees."
        )

    if station_errors:
        for error in station_errors:
            st.error(error)
    else:
        st.success(
            "Ground station configuration validated successfully!"
        )

    # ==========================================
    # SLANT RANGE VS ELEVATION ANGLE
    # ==========================================

    st.divider()

    st.header("📈 Slant Range vs. Elevation Angle")

    st.write(
        "This graph shows how the distance between "
        "the satellite and ground station changes "
        "with elevation angle."
    )

    if orbit_errors or station_errors:
        st.warning(
            "Correct the orbit and ground station "
            "inputs before generating the graph."
        )

    else:
        R = EARTH_RADIUS_KM
        h = orbit_altitude

        # Generate elevation angles from 0 to 90 degrees
        elevation_angles = np.linspace(0, 90, 100)

        slant_ranges = []

        for elevation in elevation_angles:

            elevation_rad = math.radians(
                float(elevation)
            )

            # Slant range from spherical-Earth geometry
            slant_range_km = (
                math.sqrt(
                    (R + h) ** 2
                    - (R * math.cos(elevation_rad)) ** 2
                )
                - R * math.sin(elevation_rad)
            )

            slant_ranges.append(slant_range_km)

        # Create interactive Plotly graph
        elevation_fig = go.Figure()

        elevation_fig.add_trace(
            go.Scatter(
                x=elevation_angles,
                y=slant_ranges,
                mode="lines",
                name="Slant Range",
                line=dict(width=3)
            )
        )

        # Ground station minimum elevation limit
        elevation_fig.add_vline(
            x=min_elevation,
            line_dash="dash",
            line_color="red",
            annotation_text="Minimum Elevation"
        )

        elevation_fig.update_layout(
            title="Slant Range vs. Elevation Angle",
            xaxis_title="Elevation Angle (degrees)",
            yaxis_title="Slant Range (km)",
            template="plotly_white",
            hovermode="x unified"
        )

        st.plotly_chart(
            elevation_fig,
            use_container_width=True
        )

        # Display important geometric cases
        zenith_range = calculate_slant_range(
            h, 0
        )

        horizon_angle = math.degrees(
            math.acos(R / (R + h))
        )

        horizon_range = calculate_slant_range(
            h, horizon_angle
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Zenith Slant Range",
                f"{zenith_range:.2f} km"
            )

        with col2:
            st.metric(
                "Horizon Slant Range",
                f"{horizon_range:.2f} km"
            )

        st.caption(
            "Assumptions: spherical Earth (R = 6371 km), "
            "ground station at sea level, no atmospheric "
            "refraction, and geometric line of sight."
        )
