from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from pylab import *
import pandas


cell = 5781

points = pandas.read_csv(f'C:\Environments\HTMAI\Output\cell{cell}.csv')

fig = plt.figure()
fig.suptitle(f'Cell {cell} Activation: "Strict Border"')
ax = fig.add_subplot(111, projection='3d')

x = points['x'].values
y = points['y'].values
z = points['head direction'].values

colmap = cm.ScalarMappable(cmap=cm.plasma)
colmap.set_array(z)

# creating the heatmap
img = ax.scatter(x, y, z, c=cm.plasma(z/max(z)), marker='o', s=6)

cb = fig.colorbar(colmap)
cb.set_label('Head Direction (\N{DEGREE SIGN})')

ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_zlabel('Head Direction (\N{DEGREE SIGN})')


#ax.view_init(-90,-90)     #xy
#ax.view_init(0,-90)     #xz
#ax.view_init(0, 0)     #yz


plt.show()