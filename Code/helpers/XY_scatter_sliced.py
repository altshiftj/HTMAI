import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import RangeSlider
from pathlib import Path

CELL_NUMBER = 64
LAYER = 'L4'
CELL_TYPE = 'Active'
DPI = 100

# Construct the file path
base_directory = Path(__file__).parent.parent.parent
folder_path = base_directory / "Output"
read_path =  folder_path / f'Layer Activity\\{LAYER}_{CELL_TYPE}\\cell{CELL_NUMBER}.csv'

# Check if the file exists, read the CSV file
if os.path.exists(read_path):
    df = pd.read_csv(read_path)
else:
    print(f'No cell {CELL_NUMBER} file')
    exit()

# Create the figure and set its title
fig = plt.figure(dpi=DPI)
fig.suptitle(f'Layer {LAYER}: Cell {CELL_NUMBER} Activation')

# Extract the x, y, and head direction values from the DataFrame
x = df['x'].values
y = df['y'].values
z = df['head direction'].values

# Set the x and y axis labels
plt.xlabel('X Position', fontsize='small')
plt.ylabel('Y Position')

# Create the scatter plot and invert the y-axis
scatter, = plt.plot(x, y, 'bo', markersize=2)
plt.gca().invert_yaxis()

# Create the range slider for head direction
slider_ax = plt.axes([0.20, 0.015, 0.60, 0.015])
slider = RangeSlider(slider_ax, "Head Direction", 0, 360, (0, 360), valstep=10)

# Update the scatter plot based on the range slider values
def update(val):
    df_new = df.loc[(df['head direction'] >= slider.val[0]) & (df['head direction'] <= slider.val[1])]
    x = df_new['x'].values
    y = df_new['y'].values

    scatter.set_xdata(x)
    scatter.set_ydata(y)

    fig.canvas.draw_idle()

# Add the update function to the range slider
slider.on_changed(update)
plt.show()