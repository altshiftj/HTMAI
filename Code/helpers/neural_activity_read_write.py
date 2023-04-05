import pandas as pd
import os
from pathlib import Path
import csv
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from matplotlib import cm

"""
This script processes and visualizes cell activity data from cortical column layers in the HTM 
(Hierarchical Temporal Memory) model. It reads the cell activation data from a CSV file, organizes and saves the data 
by layer and cell number, and generates 3D scatter plots of the cell activations for different orientations 
(3D, XY, XZ, YZ planes).

Functions:
- initialize_output(): Initializes the CSV output file with a header.
- write_active_cells_to_csv(): Writes active cell data to a CSV file.
- sort_cell_activity(): Sorts and saves cell activity data by layer and cell number.
- save_3d_scatters(): Creates 3D scatter plots and saves them as PNG files.
"""

base_directory = Path(__file__).parent.parent.parent
folder_path = base_directory / "Output"
file_path = folder_path / "active_cells.csv"

CSV_HEADER = ['layer', 'thought count', 'cell', 'column', 'x', 'y', 'head direction', 'speed', 'angular_velocity']
LAYERS = ['L23', 'L4', 'L6a']
CELL_TYPE = 'active'


def initialize_output():
    """
    Function to initialize the csv output file with a header
    """

    # open the file for writing in write mode, which will overwrite the file if it already exists
    with open(file_path, 'w', newline='') as f:
        # create a csv writer
        writer = csv.writer(f)

        # write the CSV_HEADER to the csv file
        writer.writerow(CSV_HEADER)

    return


def write_active_cells_to_csv(tm, layer_name, thought_count, x, y, head_direction, speed, angular_velocity):
    """
    Function to write active cell data to a csv file
    :param tm                   (TemporalMemory): temporal memory of the cortical column layer
    :param layer_name           (str): name of the layer
    :param thought_count        (int): current thought count
    :param x                    (int): x position of the animal
    :param y                    (int): y position of the animal
    :param head_direction       (int): head direction of the animal in degrees
    :param speed                (int): speed of the animal
    :param angular_velocity     (int): angular velocity of the animal
    """

    # open the file for writing in append mode
    with open(file_path, 'a', newline='') as f:
        # create a csv writer
        writer = csv.writer(f)

        # get the list of active cells from the temporal memory
        active_cells = tm.getActiveCells().sparse

        # iterate over all the active cells
        for i in range(len(active_cells)):
            # get the column for the current cell
            column = tm.columnForCell(active_cells[i])

            # create a list of data for the current cell
            data = [layer_name, thought_count, active_cells[i], column, x, y, head_direction, speed, angular_velocity]

            # write the data to the csv file
            writer.writerow(data)

    return


def sort_cell_activity(column_width, layer_depth):
    """
    Function to sort and save cell activity data by layer and cell number
    :param column_width     (int): number of minicolumns in a cortical column layer
    :param layer_depth      (int): number of cells in a minicolumn
    """

    # read in the cell activity data from the file_path
    df = pd.read_csv(file_path)

    # iterate over all the layers
    for layer in LAYERS:
        # create write directory for the current layer and cell type
        write_path = Path(f'{folder_path}/Layer Activity/{layer}_{CELL_TYPE}')
        write_path.mkdir(parents=True, exist_ok=True)

        # get the data for the current layer and cell type
        layer_data = df.loc[df['layer'] == f'{layer}_{CELL_TYPE}']

        # iterate over the first cells of each minicolumn
        for i in range(column_width):
            j = i * layer_depth
            # if there is data for the current cell, save it to a csv file in the write directory
            if not layer_data.loc[layer_data['cell'] == j].empty:
                layer_data.loc[(layer_data['cell'] == j)].to_csv(write_path / f'cell{j}.csv', index=False)

def save_3d_scatters(box_height, box_width, column_width, layer_depth):
    """
    Function to create 3D scatter plots and save them as PNG files
    :param box_height       (int): height of the box in the simulation
    :param box_width        (int): width of the box in the simulation
    :param column_width     (int): number of minicolumns in a cortical column layer
    :param layer_depth      (int): number of cells in a minicolumn
    """

    # initialize figure properties
    fig = plt.figure(figsize=[6,5])
    dpi = 100

    # lower limit for the file size of the csv files to be plotted
    min_file_size = 0

    # iterate over all the layers
    for l in range(len(LAYERS)):
        # set read and write paths for each layer and its respective plot angles
        read_path = f'{folder_path}\Layer Activity\\{LAYERS[l]}_{CELL_TYPE}'
        write_path = f'{folder_path}\Layer Activity\\{LAYERS[l]}_{CELL_TYPE}_Plots'
        write_path_3d = f'{write_path}\\3D'
        write_path_xy = f'{write_path}\XY'
        write_path_xz = f'{write_path}\XZ'
        write_path_yz = f'{write_path}\YZ'

        # create write directories if they don't already exist
        write_path_exist = os.path.exists(write_path)
        if not write_path_exist:
            os.makedirs(write_path)
            os.makedirs(write_path_3d)
            os.makedirs(write_path_xy)
            os.makedirs(write_path_xz)
            os.makedirs(write_path_yz)

        # iterate over the first cells of each minicolumn
        for j in range(column_width):
            i = j*layer_depth
            read_file = f'{read_path}\cell{i}.csv'

            # set write file paths for each cell and its respective plot angles
            write_file_3d = f'{write_path_3d}\\3D_Cell_{i}.png'
            write_file_xy = f'{write_path_xy}\XY_Cell_{i}.png'
            write_file_xz = f'{write_path_xz}\XZ_Cell_{i}.png'
            write_file_yz = f'{write_path_yz}\YZ_Cell_{i}.png'

            # read in the csv file for the current cell if it exists and is larger than the minimum file size
            if os.path.exists(read_file) and os.path.getsize(read_file) > min_file_size:
                df = pd.read_csv(read_file)
            else:
                continue

            # if the data frame is not empty, plot its data
            if not df.empty:
                # iterate over the four plot angles
                for k in range(4):
                    # Clear the current figure
                    plt.clf()

                    # Add a title to the figure with the current layer and cell
                    fig.suptitle(f'Layer {LAYERS[l]}: Cell {i} Activation')

                    # Add a 3D plot to the figure
                    ax = fig.add_subplot(111, projection='3d')

                    # Set the x and y limits of the plot to the box width and height
                    plt.xlim(0, box_width)
                    plt.ylim(0, box_height)

                    # Get the x, y, and z values from the data frame
                    x = df['x'].values
                    y = df['y'].values
                    z = df['head direction'].values

                    # Create a color map based on the head direction values
                    colmap = cm.ScalarMappable(cmap=cm.plasma)
                    colmap.set_array(z)

                    # Set up the plot settings for the 3D plot
                    img = ax.scatter(x, y, z, c=cm.plasma(z / max(z)), marker='o', s=6)

                    # Add a color bar to the plot
                    cb = fig.colorbar(colmap, ax=ax, fraction=0.033)
                    cb.set_label('Head Direction (\N{DEGREE SIGN})')

                    # Add axis labels and tick marks to the plot
                    ax.set_xlabel('X Position')
                    ax.set_ylabel('Y Position')
                    ax.set_zlabel('Head Direction (\N{DEGREE SIGN})')
                    ax.tick_params(axis='both', which='major', labelsize=6)
                    ax.tick_params(axis='both', which='minor', labelsize=6)

                    # Match the current view of the plot to one of the 4 cases
                    match k:
                        # Case 0: Default 3D plot
                        case 0:
                            ax.set_zlabel('')
                            plt.tight_layout()
                            plt.savefig(write_file_3d, dpi=dpi)
                            plt.clf()

                        # Case 1: xy plane view
                        case 1:
                            ax.view_init(-90, -90)  # xy
                            ax.set_zticks([])
                            ax.set_zlabel('')
                            plt.tight_layout()
                            plt.savefig(write_file_xy, dpi=dpi)
                            plt.clf()

                        # Case 2: xz plane view
                        case 2:
                            ax.view_init(0, -90)  # xz
                            ax.set_yticks([])
                            ax.set_ylabel('')
                            ax.set_zlabel('')
                            plt.tight_layout()
                            plt.savefig(write_file_xz, dpi=dpi)
                            plt.clf()

                        # Case 3: yz plane view
                        case 3:
                            ax.view_init(0, 0)  # yz
                            ax.set_xticks([])
                            ax.set_xlabel('')
                            plt.tight_layout()
                            plt.savefig(write_file_yz, dpi=dpi)
                            plt.clf()