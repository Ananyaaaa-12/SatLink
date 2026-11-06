
import math

EARTH_RADIUS_KM = 6371.0


def calculate_slant_range(
    altitude_km: float,
    separation_angle_deg: float
) -> float:
    """
    Calculate satellite-to-ground slant range
    using spherical-Earth geometry.

    Parameters:
        altitude_km: Satellite altitude in km.
        separation_angle_deg: Geocentric separation
            angle in degrees.

    Returns:
        Slant range in km.
    """

    if not math.isfinite(altitude_km) or altitude_km <= 0:
        raise ValueError(
            "Satellite altitude must be positive."
        )

    if (
        not math.isfinite(separation_angle_deg)
        or not 0 <= separation_angle_deg <= 180
    ):
        raise ValueError(
            "Separation angle must be between 0 and 180 degrees."
        )

    R = EARTH_RADIUS_KM
    r = R + altitude_km

    angle_rad = math.radians(separation_angle_deg)

    distance_squared = (
        R**2
        + r**2
        - 2 * R * r * math.cos(angle_rad)
    )

    return math.sqrt(max(distance_squared, 0.0))
