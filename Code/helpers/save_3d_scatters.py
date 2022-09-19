from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from pylab import *
import pandas
import os

def save_3d_scatters():
    fig = plt.figure()
    layers = [
        'L23',
        'L4',
        'L5a',
        'L5b',
        'L6a',
        'L6b'
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
            i = j * 32
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
                for k in range(1):
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

                    cb = fig.colorbar(colmap)
                    cb.set_label('Head Direction (\N{DEGREE SIGN})')

                    ax.set_xlabel('X Position')
                    ax.set_ylabel('Y Position')
                    ax.set_zlabel('Head Direction (\N{DEGREE SIGN})')

                    ax.tick_params(axis='both', which='major', labelsize=7)
                    ax.tick_params(axis='both', which='minor', labelsize=7)

                    match k:
                        case 3:
                            plt.savefig(write_file_3d, dpi=dpi)
                            plt.clf()

                        case 0:
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