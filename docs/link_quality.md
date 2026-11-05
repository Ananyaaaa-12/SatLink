# SatLink Receiver Noise & Link Quality Engine (Day 2 & Day 3)

## Mathematical Formulations
- Thermal Noise: N = k * T * B
- Noise Spectral Density: N0 = k * T
- Carrier-to-Noise Density: C/N0 = C (dBW) - 10 * log10(k * T)
- Energy per Bit: Eb/N0 = C/N0 - 10 * log10(Rb)
- Link Margin: Margin = Available Eb/N0 - Required Eb/N0

## Reference Validation Case (2.2 GHz, 1000 km, 10 W, T=290 K)
- EIRP: 25.00 dBW
- FSPL: 159.31 dB
- Received Power: -101.31 dBW (-71.31 dBm)
- C/N0: 102.67 dB-Hz
- Available Eb/N0: 42.67 dB
- Link Margin (Req: 10 dB): +32.67 dB (Status: PASS)
