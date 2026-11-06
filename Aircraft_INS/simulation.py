import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. SIMULATION SETTINGS
# ============================================================

dt = 0.1
total_time = 60

time = np.arange(0, total_time, dt)


# ============================================================
# 2. INITIAL AIRCRAFT CONDITIONS
# ============================================================

initial_position = np.array([0.0, 0.0, 10000.0])
initial_velocity = np.array([200.0, 0.0, 0.0])


# ============================================================
# 3. CREATE ARRAYS
# ============================================================

n = len(time)

position = np.zeros((n, 3))
velocity = np.zeros((n, 3))
acceleration = np.zeros((n, 3))

# Attitude: roll, pitch, yaw
attitude = np.zeros((n, 3))

# Angular rates: roll rate, pitch rate, yaw rate
angular_rate = np.zeros((n, 3))


# Set initial conditions
position[0] = initial_position
velocity[0] = initial_velocity


# ============================================================
# 4. SIMULATE AIRCRAFT ATTITUDE
# ============================================================

for i in range(n):

    t = time[i]

    # --------------------------------------------------------
    # ROLL
    # --------------------------------------------------------

    if t < 10:
        roll = 0.0

    elif t < 15:
        # Roll from 0° to 20°
        roll = np.deg2rad(20) * (t - 10) / 5

    elif t < 35:
        # Maintain 20° bank
        roll = np.deg2rad(20)

    elif t < 40:
        # Return from 20° to 0°
        roll = np.deg2rad(20) * (1 - (t - 35) / 5)

    else:
        roll = 0.0


    # --------------------------------------------------------
    # PITCH
    # --------------------------------------------------------

    if t < 20:
        pitch = np.deg2rad(2) * (t / 20)

    elif t < 40:
        pitch = np.deg2rad(2)

    else:
        pitch = np.deg2rad(2) * (1 - (t - 40) / 20)


# --------------------------------------------------------
# YAW
# --------------------------------------------------------

g = 9.81
V = np.linalg.norm(initial_velocity)

if t < 15:
    yaw = 0.0

elif t < 35:
    # Coordinated turn:
    # yaw_rate = g * tan(bank_angle) / velocity

    turn_rate = g * np.tan(roll) / V

    yaw = turn_rate * (t - 15)

elif t < 40:
    turn_rate = g * np.tan(np.deg2rad(20)) / V

    yaw = turn_rate * 20

else:
    yaw = turn_rate * 20

    attitude[i] = [roll, pitch, yaw]


# ============================================================
# 5. CALCULATE ANGULAR RATES
# ============================================================

# Numerical derivative of attitude
angular_rate[:, 0] = np.gradient(attitude[:, 0], dt)
angular_rate[:, 1] = np.gradient(attitude[:, 1], dt)
angular_rate[:, 2] = np.gradient(attitude[:, 2], dt)


# ============================================================
# 6. SIMULATE AIRCRAFT TRANSLATIONAL MOTION
# ============================================================

for i in range(1, n):

    t = time[i]

    # Forward acceleration
    ax = 0.5

    # Small vertical acceleration
    az = 0.2 * np.sin(0.1 * t)

    # Lateral acceleration produced by the bank angle
if 15 <= t <= 35:
    ay = 9.81 * np.tan(attitude[i, 0])
else:
    ay = 0.0

    acceleration[i] = np.array([ax, ay, az])

    # Update velocity
    velocity[i] = (
        velocity[i - 1]
        + acceleration[i] * dt
    )

    # Update position
    position[i] = (
        position[i - 1]
        + velocity[i - 1] * dt
        + 0.5 * acceleration[i] * dt**2
    )


# ============================================================
# 7. PLOT POSITION
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(time, position[:, 0], label="X Position")
plt.plot(time, position[:, 1], label="Y Position")
plt.plot(time, position[:, 2], label="Altitude")

plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Aircraft True Position")

plt.legend()
plt.grid()

plt.show()


# ============================================================
# 8. PLOT VELOCITY
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(time, velocity[:, 0], label="X Velocity")
plt.plot(time, velocity[:, 1], label="Y Velocity")
plt.plot(time, velocity[:, 2], label="Vertical Velocity")

plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title("Aircraft True Velocity")

plt.legend()
plt.grid()

plt.show()


# ============================================================
# 9. PLOT ATTITUDE
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    time,
    np.rad2deg(attitude[:, 0]),
    label="Roll"
)

plt.plot(
    time,
    np.rad2deg(attitude[:, 1]),
    label="Pitch"
)

plt.plot(
    time,
    np.rad2deg(attitude[:, 2]),
    label="Yaw"
)

plt.xlabel("Time (s)")
plt.ylabel("Angle (degrees)")
plt.title("Aircraft True Attitude")

plt.legend()
plt.grid()

plt.show()


# ============================================================
# 10. PLOT ANGULAR RATES
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    time,
    np.rad2deg(angular_rate[:, 0]),
    label="Roll Rate"
)

plt.plot(
    time,
    np.rad2deg(angular_rate[:, 1]),
    label="Pitch Rate"
)

plt.plot(
    time,
    np.rad2deg(angular_rate[:, 2]),
    label="Yaw Rate"
)

plt.xlabel("Time (s)")
plt.ylabel("Angular Rate (degrees/s)")
plt.title("Aircraft True Angular Rates")

plt.legend()
plt.grid()

plt.show()