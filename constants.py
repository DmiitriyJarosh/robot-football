# Variables for movement algorithm
ro_start = 0
alpha_start = 0
beta_start = 0

# Starting wheel velocities
vl_start = 0.00
vr_start = 0.00

# A starting pose of robot
x_start = -4.0
y_start = -2.5
theta_start = 0

# Constants for movement algorithm
k_ro = 0.5
k_alpha = 5
k_beta = 1
l = -0.1
r = 1

# Constants
MAXVELOCITY = 0.3  # ms^(-1) max speed of each wheel
WINDOW_CORNERS = (-4.0, -2.5, 4.0, 2.5)  # The region we will fill with obstacles

# Constants for graphics display
# Transformation from metric world frame to graphics frame
# k pixels per metre
# Horizontal screen coordinate:     u = u0 + k * x
# Vertical screen coordinate:       v = v0 - k * y

# Set the width and height of the screen (pixels)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500


class Color:
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (20, 20, 40)
    GREY = (70, 70, 70)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    LIGHTBLUE = (0, 120, 255)


k = 100  # pixels per metre for graphics

