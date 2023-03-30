from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import os
import csv

f = open('cell_fire.csv', 'w', newline='')
writer = csv.writer(f)

def initialize_csv():
    header = ['layer', 'thought count', 'cell', 'column', 'x', 'y', 'head direction', 'linear_speed', 'angular_velocity']
    writer.writerow(header)

def write_activecell_to_csv(tm, layer_name, thought_count, x, y, head_direction, linear_speed, angular_velocity):
    active_cells = tm.getActiveCells().sparse
    for i in range(len(active_cells)):
        column = tm.columnForCell(active_cells[i])
        data = [layer_name, thought_count, active_cells[i], column, x, y, head_direction, linear_speed, angular_velocity]
        writer.writerow(data)
    return

def write_predcell_to_csv(tm, sdr, layer_name, thought_count, x, y, head_direction, linear_speed, angular_velocity):
    predictive_cells = sdr.sparse
    for i in range(len(predictive_cells)):
        column = tm.columnForCell(predictive_cells[i])
        data = [layer_name, thought_count, predictive_cells[i], column, x, y, head_direction, linear_speed, angular_velocity]
        writer.writerow(data)
    return

def write_winnercell_to_csv(tm, layer_name, thought_count, x, y, head_direction, linear_speed, angular_velocity):
    winner_cells = tm.getWinnerCells().sparse
    for i in range(len(winner_cells)):
        column = tm.columnForCell(winner_cells[i])
        data = [layer_name, thought_count, winner_cells[i], column, x, y, head_direction, linear_speed, angular_velocity]
        writer.writerow(data)
    return

def save_3d_scatters():
    fig = plt.figure(figsize=[6,5], layout='tight')
    layers = [
        'L23',
        'L4',
        'L6a'
        ]

    min_file_size = 0

    cell_type = 'Active'
    dpi = 100

    for l in range(len(layers)):

        read_path = f'C:\Environments\HTMAI Output\\{layers[l]}_{cell_type}'
        write_path = f'C:\Environments\HTMAI Output\\{layers[l]}_{cell_type}_Plots'

        write_path_3d = f'{write_path}\\3D'
        write_path_xy = f'{write_path}\XY'
        write_path_xz = f'{write_path}\XZ'
        write_path_yz = f'{write_path}\YZ'

        write_path_exist = os.path.exists(write_path)
        if not write_path_exist:
            os.makedirs(write_path)
            os.makedirs(write_path_3d)
            os.makedirs(write_path_xy)
            os.makedirs(write_path_xz)
            os.makedirs(write_path_yz)

        for j in range(256):
            i = j*32
            read_file = f'{read_path}\cell{i}.csv'

            write_file_3d = f'{write_path_3d}\\3D_Cell_{i}.png'
            write_file_xy = f'{write_path_xy}\XY_Cell_{i}.png'
            write_file_xz = f'{write_path_xz}\XZ_Cell_{i}.png'
            write_file_yz = f'{write_path_yz}\YZ_Cell_{i}.png'

            if os.path.exists(read_file) and os.path.getsize(read_file) > min_file_size:
                df = pandas.read_csv(read_file)
            else:
                continue

            if not df.empty:
                for k in range(4):
                    plt.clf()
                    fig.suptitle(f'Layer {layers[l]}: Cell {i} Activation')
                    ax = fig.add_subplot(111, projection='3d')
                    plt.xlim(0,1600)
                    plt.ylim(0,1600)

                    x = df['x'].values
                    y = df['y'].values
                    z = df['head direction'].values

                    colmap = cm.ScalarMappable(cmap=cm.plasma)
                    colmap.set_array(z)

                    img = ax.scatter(x, y, z, c=cm.plasma(z / max(z)), marker='o', s=6)

                    cb = fig.colorbar(colmap, fraction=0.033)
                    cb.set_label('Head Direction (\N{DEGREE SIGN})')

                    ax.set_xlabel('X Position')
                    ax.set_ylabel('Y Position')
                    ax.set_zlabel('Head Direction (\N{DEGREE SIGN})')

                    ax.tick_params(axis='both', which='major', labelsize=6)
                    ax.tick_params(axis='both', which='minor', labelsize=6)

                    match k:
                        case 0:
                            ax.set_zlabel('')
                            plt.savefig(write_file_3d, dpi=dpi)
                            plt.clf()

                        case 1:
                            ax.view_init(-90, -90)  # xy
                            ax.set_zticks([])
                            ax.set_zlabel('')
                            plt.savefig(write_file_xy, dpi=dpi)
                            plt.clf()

                        case 2:
                            ax.view_init(0, -90)  # xz
                            ax.set_yticks([])
                            ax.set_ylabel('')
                            ax.set_zlabel('')
                            plt.savefig(write_file_xz, dpi=dpi)
                            plt.clf()

                        case 3:
                            ax.view_init(0, 0)  # yz
                            ax.set_xticks([])
                            ax.set_xlabel('')
                            plt.savefig(write_file_yz, dpi=dpi)
                            plt.clf()