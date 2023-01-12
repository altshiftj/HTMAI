import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import RangeSlider
import pandas
import os


cell_number = 416
layer = 'L4'
cell_type = 'Active'
dpi = 100

read_path = f'C:\Environments\HTMAI Output\\{layer}_{cell_type}\cell{cell_number}.csv'

read_path_exist = os.path.exists(read_path)

if os.path.exists(read_path):
    df = pandas.read_csv(read_path)
    data = df.to_numpy()
else:
    print(f'No cell {layer}-{cell_number} file')
    exit()

fig = plt.figure(dpi=dpi)
fig.suptitle(f'Layer {layer}: Cell {cell_number} Activation')

x = df['x'].values
y = df['y'].values
z = df['head direction'].values



plt.xlabel('X Position', fontsize='small')
plt.ylabel('Y Position')

scatter, = plt.plot(x, y, 'bo', markersize=2)
plt.gca().invert_yaxis()

slider_ax = plt.axes([0.20, 0.015, 0.60, 0.015])
slider = RangeSlider(slider_ax, "Head Direction", 0, 360, (0,360), valstep=10)

def update(val):
    df_new = df.loc[(df['head direction'] >= slider.val[0]) & (df['head direction'] <= slider.val[1])]
    x = df_new['x'].values
    y = df_new['y'].values

    scatter.set_xdata(x)
    scatter.set_ydata(y)

    fig.canvas.draw_idle()

slider.on_changed(update)
plt.show()