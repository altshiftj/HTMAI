from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from pylab import *
import pandas

fig = plt.figure()


for i in range(256*32):
    j=i*32
    df = pandas.read_csv(f'C:\Environments\HTMAI\Code\Output\L6a_Active\column{i}_cell{j}.csv')

    if not df.empty:
        for k in range(4):

            fig.suptitle(f'Cell {j} Activation')
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
                # case 0:
                #     plt.savefig(f'C:\Environments\HTMAI\Code\Output\L4_Plots\\3D_Cell_{j}.png', dpi=250)
                #     plt.clf()

                case 1:
                    ax.view_init(-90, -90)  # xy
                    plt.savefig(f'C:\Environments\HTMAI\Code\Output\L6a_Active_Plots\XY_Cell_{j}.png', dpi=250)
                    plt.clf()

                # case 2:
                #     ax.view_init(0, -90)  # xz
                #     plt.savefig(f'C:\Environments\HTMAI\Code\Output\L4_Plots\XZ_Cell_{j}.png', dpi=250)
                #     plt.clf()
                #
                # case 3:
                #     ax.view_init(0, 0)  # yz
                #     plt.savefig(f'C:\Environments\HTMAI\Code\Output\L4_Plots\YZ_Cell_{j}.png', dpi=250)
                #     plt.clf()