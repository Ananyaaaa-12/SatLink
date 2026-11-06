import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# SENSOR SETTINGS
# ============================================================

# Accelerometer bias in m/s²
ACCEL_BIAS = np.array([
    0.05,
    -0.03,
    0.02
])

# Gyroscope bias in degrees/s
GYRO_BIAS_DEG = np.array([
    0.10,
    -0.05,
    0.08
])

# Convert gyro bias to radians/s
GYRO_BIAS = np.deg2rad(GYRO_BIAS_DEG)


# Random noise levels
ACCEL_NOISE_STD = 0.03
GYRO_NOISE_STD = np.deg2rad(0.05)


# ============================================================
# LOAD TRUE AIRCRAFT DATA
# ============================================================

# Import the simulation
import simulation

time = simulation.time
true_acceleration = simulation.acceleration
true_angular_rate = simulation.angular_rate


# ============================================================
# GENERATE SENSOR MEASUREMENTS
# ============================================================

np.random.seed(42)

n = len(time)


# Accelerometer noise
accelerometer_noise = np.random.normal(
    0,
    ACCEL_NOISE_STD,
    size=(n, 3)
)


# Gyroscope noise
gyroscope_noise = np.random.normal(
    0,
    GYRO_NOISE_STD,
    size=(n, 3)
)


# Sensor measurements
accelerometer_measurement = (
    true_acceleration
    + ACCEL_BIAS
    + accelerometer_noise
)


gyroscope_measurement = (
    true_angular_rate
    + GYRO_BIAS
    + gyroscope_noise
)


# ============================================================
# PLOT ACCELEROMETER
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    time,
    true_acceleration[:, 0],
    label="True X Acceleration"
)

plt.plot(
    time,
    accelerometer_measurement[:, 0],
    label="Measured X Acceleration",
    alpha=0.7
)

plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s²)")
plt.title("Accelerometer: True vs Measured")

plt.legend()
plt.grid()

plt.show()


# ============================================================
# PLOT GYROSCOPE
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    time,
    np.rad2deg(true_angular_rate[:, 0]),
    label="True Roll Rate"
)

plt.plot(
    time,
    np.rad2deg(gyroscope_measurement[:, 0]),
    label="Measured Roll Rate",
    alpha=0.7
)

plt.xlabel("Time (s)")
plt.ylabel("Angular Rate (degrees/s)")
plt.title("Gyroscope: True vs Measured")

plt.legend()
plt.grid()

plt.show()