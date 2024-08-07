"""
This is the ECEF to ECI Convertor for the power model

"""

from datetime import datetime

from numpy.typing import NDArray
import numpy as np


## ECEF to ECI Conversion from https://github.com/eribean/Geneci
def ecef_to_eci(
    self,
    ecef_point: NDArray[np.float64],
    utc_time: datetime,
    ecef_velocity: NDArray[np.float64] = None,
) -> NDArray[np.float64] | tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Convert ECEF point/velocity to ECI point/velocity.

    Args:
        ecef_point (NDArray[np.float64]): (3,) 1-d vector describing ECEF point [X, Y, Z]
        utc_time (datetime): Observed time of position and/or velocity
        ecef_velocity (NDArray[np.float64]): (3,) 1-d vector describing ECEF velocity [Vx, Vy, Vz]

    Returns:
        eci_point (NDArray[np.float64]): (3,) 1-d vector describing ECI point [X, Y, Z]
            eci_velocity (NDArray[np.float64]): (3,) 1-d vector describing ECI velocity [Vx, Vy, Vz]

    Note:
        The velocity is only returned if a velocity is supplied
    """
    # Convert the utc time to julian day, then to century
    julian_day = self.utc_time_to_julian_date(utc_time)
    julian_century = (julian_day - 2451545.0) / 36525.0  # Eq. 5.2

    # Get the rotation matrix
    rotation_ecef_to_eci = self.rotation_matrix_ecef_to_eci(julian_century)

    # Rotate the position
    eci_point = rotation_ecef_to_eci @ ecef_point

    # Rotate the velocity if it is supplied
    if ecef_velocity is not None:
        eci_velocity = (
            rotation_ecef_to_eci @ ecef_velocity
            + (rotation_ecef_to_eci @ self.DERIVATIVE_MATRIX) @ ecef_point
        )
        return eci_point, eci_velocity


def rotation_matrix_ecef_to_eci(self, julian_century: float) -> NDArray[np.float64]:
    """Return ecef to eci rotation matrix for a given time.

    Rotation is applied to the vector components.

    P_eci = R(t) @ P_ecef

    Args:
        julian_date (float): Time in Julian centuries.
     Returns:
        rotation_matrx (NDArray[float]): 3x3 Matrix to rotate ECEF to ECI
    """
    # Angular motion of the earth
    earth_rotation_angle = (
        2 * np.pi * (0.7790572732640 + 1.00273781191135448 * 36525.0 * julian_century)
    )
    earth_matrix = np.eye(3)
    earth_matrix[0, 0] = earth_matrix[1, 1] = np.cos(earth_rotation_angle)
    earth_matrix[1, 0] = np.sin(earth_rotation_angle)
    earth_matrix[0, 1] = -1 * earth_matrix[1, 0]

    # Precession / Nutation rotation matrix (Eq. 5.10)
    gcrs_x, gcrs_y = self.compute_celestial_positions(julian_century)
    a = 0.5 + 0.125 * (gcrs_x * gcrs_x + gcrs_y * gcrs_y)

    pn_matrix = np.array(
        [
            [1 - a * gcrs_x * gcrs_x, -a * gcrs_x * gcrs_y, gcrs_x],
            [-a * gcrs_x * gcrs_y, 1 - gcrs_y * gcrs_y, gcrs_y],
            [-gcrs_x, -gcrs_y, 1 - a * (gcrs_x * gcrs_x + gcrs_y * gcrs_y)],
        ]
    )

    # Return the rotation
    return pn_matrix @ earth_matrix


## The monstrosity that is the nutation / precession
def compute_celestial_positions(self, julian_century: float) -> tuple[float, float]:
    """Compute the x-y components of the celestial pole in earth reference frame.

    Args:
        julian_date (float): Time in Julian centuries.

    Returns:
        celestial_x (float): x-component of the pole vector in radians
        celestial_y (float): y-component of the pole vector in radians

    """
    celestial_x = self.precession_x(julian_century)
    celestial_y = self.precession_y(julian_century)

    # Update for nutation (Coeffients are micro arc-seconds)
    omega = self.moon_ascension(julian_century) * self.ARC_SECONDS_TO_RADIANS
    D = self.moon_elongation(julian_century) * self.ARC_SECONDS_TO_RADIANS
    F = self.moon_longitude(julian_century) * self.ARC_SECONDS_TO_RADIANS
    l_prime = self.sun_anomoly(julian_century) * self.ARC_SECONDS_TO_RADIANS

    # Precompute reoccuring argument
    f_omega_d = 2 * (F + omega - D)

    celestial_x += 1e-6 * (
        (
            -6844318.44 * np.sin(omega)
            - 523908.04 * np.sin(f_omega_d)
            - 90552.22 * np.sin(2 * (F + omega))
            + 82168.76 * np.sin(2 * omega)
            + 58707.02 * np.sin(l_prime)
        )
        + julian_century * (205833.11 * np.cos(omega) + 12814.01 * np.cos(f_omega_d))
    )

    celestial_y += 1e-6 * (
        (
            9205236.26 * np.cos(omega)
            + 573033.42 * np.cos(f_omega_d)
            + 97846.69 * np.cos(2 * (F + omega))
            - 89618.24 * np.cos(2 * omega)
            + 22438.42 * np.cos(l_prime - f_omega_d)
        )
        + julian_century * (153041.79 * np.sin(omega) + 11714.49 * np.sin(f_omega_d))
    )

    return (
        celestial_x * self.ARC_SECONDS_TO_RADIANS,
        celestial_y * self.ARC_SECONDS_TO_RADIANS,
    )


def utc_time_to_julian_date(self, utc_time: datetime) -> float:
    """Convert UTC time to Julian date.

    This calculation is only valid for days after March 1900.

    Args:
        utc_time (datetime): The observation time as a datetime object

    Returns:
        julian_date (float): The observation time as a julian date.
    """
    year, month, day = utc_time.year, utc_time.month, utc_time.day
    julian_date = (
        367 * year
        - 7 * (year + (month + 9) // 12) // 4
        + 275 * month // 9
        + day
        + 1721013.5
    )

    # update with the frational day
    julian_date += (
        utc_time.hour
        + utc_time.minute / 60
        + (utc_time.second + 1e-6 * utc_time.microsecond) / 3600
    ) / 24

    return julian_date
