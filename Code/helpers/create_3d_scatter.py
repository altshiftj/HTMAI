from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from pylab import *
import pandas

layer = 'L4'
cell_type = 'Active'
column = 11
cell = column * 32
df = pandas.read_csv(f'C:\Environments\HTMAI\Code\Output\\{layer}_{cell_type}\column{column}_cell{cell}.csv')

x = df['x'].values
y = df['y'].values
z = df['head direction'].values

fig = plt.figure()

fig.suptitle(f'Cell {cell} Activation')
ax = fig.add_subplot(111, projection='3d')

colmap = cm.ScalarMappable(cmap=cm.plasma)
colmap.set_array(z)

img = ax.scatter(x, y, z, c=cm.plasma(z / max(z)), marker='o', s=6)

axz = plt.axes([0.25, 0.15, 0.65, 0.03])

cb = fig.colorbar(colmap)
cb.set_label('Head Direction (\N{DEGREE SIGN})')

ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_zlabel('Head Direction (\N{DEGREE SIGN})')

zslide = Slider(axz, 'Head Direction', 0, 360, 180)

def update(val):
    zval = zslide.val
    ax.set_zlim3d(zval-.5,zval+.5)


zslide.on_changed(update)

plt.show()