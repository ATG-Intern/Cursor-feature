import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

matplotlib.use('TkAgg')

def calculate_3D_distance(x1, y1, z1, x0, y0, z0):
    return np.sqrt((x1-x0)**2 + (y1-y0)**2 + (z1-z0)**2)

def update_plot():
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_zlim(0, 10)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title("Click to select two points in 3D space")

def on_click(event):
    global points, z_coords
    if len(points) < 2:
        points.append((event.xdata, event.ydata))
        if len(points) == 2:
            z_coords = np.random.uniform(0, 10, 2)
            x0, y0 = points[0]
            x1, y1 = points[1]
            z0, z1 = z_coords

            ax.scatter(x0, y0, z0, c='r', marker='o')
            ax.scatter(x1, y1, z1, c='g', marker='o')
            ax.plot([x0, x1], [y0, y1], [z0, z1])

            distance = calculate_3D_distance(x1, y1, z1, x0, y0, z0)
            plt.figtext(0.5, 0.01, f"Distance: {distance:.2f}", ha="center", fontsize=12)

            fig.canvas.draw()
    else:
        points = []
        z_coords = []
        update_plot()
        distance = 0
        plt.figtext(0.5, 0.01, f"Distance:", ha="center", fontsize=12)
        fig.canvas.draw()

plt.ion()
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

update_plot()

points = []
z_coords = []

fig.canvas.mpl_connect('button_press_event', on_click)

plt.show(block=True)