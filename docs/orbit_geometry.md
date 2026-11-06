
# SatLink — Orbit Geometry Module

## Overview
This module calculates the geometric slant range
between a satellite and a ground station.

## Mathematical Model

The spherical-Earth slant range equation is:

d = sqrt(R² + (R+h)² - 2R(R+h)cos(ψ))

Where:
- R = Earth radius (6371 km)
- h = Satellite altitude (km)
- ψ = Geocentric separation angle
- d = Slant range (km)

## Assumptions
- Earth is spherical with radius 6371 km.
- Ground station is at sea level.
- Atmospheric refraction is neglected.
- Satellite altitude is measured above Earth's surface.
- The model calculates geometric distance only.
- Ground station latitude and longitude are not yet
  used for satellite position calculations.
- Orbital inclination and eccentricity are inputs,
  but orbital propagation is not yet implemented.

## Special Cases

### Zenith
At a geocentric separation angle of 0 degrees,
slant range equals satellite altitude.

### Horizon
At the geometric horizon:

ψ = acos(R / (R+h))

The slant range is:

d = sqrt(h(2R+h))

## Limitations
The function can calculate distances beyond the
geometric horizon, but those paths are obstructed
by Earth and do not represent a usable direct link.

Real satellite visibility calculations require
orbital position and ground station geometry.
