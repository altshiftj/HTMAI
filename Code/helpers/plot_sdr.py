import matplotlib.pyplot as plt
import numpy as np
from htm.bindings.sdr import SDR

"""
Define methods for plotting SDRs in the named dimensions.
"""

def plot_2d_sdr(sdr):
    # Plot the SDR as a binary image
    plt.imshow(sdr_array, cmap='binary', interpolation='nearest')

    # Show the plot
    plt.show()

def plot_3d_sdr(sdr):
    # Get the dimensions of the SDR
    dim1, dim2, dim3 = sdr.dimensions

    # Create a 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Generate data for the scatter plot
    x = np.arange(dim1)
    y = np.arange(dim2)
    z = np.arange(dim3)
    x, y, z = np.meshgrid(x, y, z)

    # Plot the data
    ax.scatter(x, y, z, c=sdr_array.flatten())

    # Show the plot
    plt.show()