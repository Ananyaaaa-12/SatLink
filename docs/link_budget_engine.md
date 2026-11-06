# SatLink Link Budget Calculation Engine

## Overview
Modular backend module performing satellite communication link budget calculations, independent of the UI layer.

## Mathematical Formulation

### 1. Free Space Path Loss (FSPL)
FSPL = 20 * log10((4 * π * d * f) / c)

- d: Slant range (m)
- f: Carrier frequency (Hz)
- c: Speed of light (299,792,458 m/s)

### 2. Effective Isotropic Radiated Power (EIRP)
EIRP = Pt (dBW) + Gt (dBi)

### 3. Received Signal Power (Pr)
Pr = EIRP + Gr - FSPL - L

- Gr: Receiving antenna gain (dBi)
- L: System losses (dB)

## Validation Case
- Frequency: 2.2 GHz
- Slant Range: 1000 km
- Transmitter Power: 10 W
- Tx Antenna Gain: 15 dBi
- Rx Antenna Gain: 35 dBi
- Additional Losses: 2 dB

| Parameter | Expected Value | Status |
| :--- | :--- | :--- |
| EIRP | 25.00 dBW | Passed |
| FSPL | 159.31 dB | Passed |
| Received Power | -71.31 dBm | Passed |
