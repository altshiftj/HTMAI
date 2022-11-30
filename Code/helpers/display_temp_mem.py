import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")

plt.ion()
figure = plt.figure()


def initialize_display(tm, tm_info):
    num_cells = tm_info.dimensions[0]
    tm_depth = tm.getCellsPerColumn()

    grid = np.zeros((num_cells, 3))

    xc = 0
    yc = 0

    for i in range(num_cells):
        if not i == 0 and i % tm_depth == 0:
            xc += 1
            yc = 0

        grid[i, 0] = xc
        grid[i, 1] = yc

        yc += 1

    return grid


def display(grid):
    marker_size = 4
    plt.scatter(grid[:, 0], grid[:, 1], c=grid[:, 2], s=30)
    figure.canvas.draw()
    figure.canvas.flush_events()


def display_active_cells(tm, tm_info):
    active_cells = tm.getActiveCells()
    grid = initialize_display(tm, tm_info)

    zval = active_cells.dense.reshape(-1)

    grid[:,2,] = zval
    display(grid)


def display_active_freq(tm, tm_info):
    active_freq = tm_info.activationFrequency.activationFrequency
    grid = initialize_display(tm, tm_info)

    zval = active_freq
    grid[:, 2] = zval

    display(grid)