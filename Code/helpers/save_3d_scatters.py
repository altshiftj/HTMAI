from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from pylab import *
import pandas
import os

fig = plt.figure()
layer = 'L6a'
cell_type = 'Active'
dpi = 225

path_L23_active =   'C:\Environments\HTMAI\Code\Output\L23_Active_Plots'
path_L4_active =    'C:\Environments\HTMAI\Code\Output\L4_Active_Plots'
path_L6a_active =    'C:\Environments\HTMAI\Code\Output\L6a_Active_Plots'

L23_exist = os.path.exists(path_L23_active)
L4_exist = os.path.exists(path_L4_active)
L6a_exist = os.path.exists(path_L6a_active)

if not L23_exist:
    os.makedirs(path_L23_active)

if not L4_exist:
    os.makedirs(path_L4_active)

if not L6a_exist:
    os.makedirs(path_L6a_active)

for i in range(256*32):
    if os.path.exists(f'C:\Environments\HTMAI\Code\Output\\{layer}_{cell_type}\cell{i}.csv'):
        df = pandas.read_csv(f'C:\Environments\HTMAI\Code\Output\\{layer}_{cell_type}\cell{i}.csv')
    else:
        continue

    if not df.empty:
        for k in range(4):
            plt.clf()
            fig.suptitle(f'Cell {i} Activation')
            ax = fig.add_subplot(111, projection='3d')

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

            match k:
                case 0:
                    plt.savefig(f'C:\Environments\HTMAI\Code\Output\\{layer}_{cell_type}_Plots\\3D_Cell_{i}.png', dpi=dpi)
                    plt.clf()

                case 1:
                    ax.view_init(-90, -90)  # xy
                    plt.savefig(f'C:\Environments\HTMAI\Code\Output\\{layer}_{cell_type}_Plots\XY_Cell_{i}.png', dpi=dpi)
                    plt.clf()

                case 2:
                    ax.view_init(0, -90)  # xz
                    plt.savefig(f'C:\Environments\HTMAI\Code\Output\\{layer}_{cell_type}_Plots\XZ_Cell_{i}.png', dpi=dpi)
                    plt.clf()

                case 3:
                    ax.view_init(0, 0)  # yz
                    plt.savefig(f'C:\Environments\HTMAI\Code\Output\\{layer}_{cell_type}_Plots\YZ_Cell_{i}.png', dpi=dpi)
                    plt.clf()