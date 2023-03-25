import matplotlib.pyplot as plt
import numpy as np
from htm.bindings.sdr import SDR

"""
Define methods for plotting SDRs in the named dimensions.
"""

def plot_2d_sdr(sdr):
    # create a numpy array from the SDR
    sdr_array = np.array(sdr.dense)

    # Plot the SDR as a binary image
    plt.imshow(sdr_array, cmap='binary', interpolation='nearest')

    # Show the plot
    plt.show()

def plot_2d_tm(tm):
    # Get the active cells of the TM
    tm_array = tm.getActiveCells()

    # Reshape the TM array
    tm_array = np.array(tm_array.dense.reshape(tm_array.dimensions[1], tm_array.dimensions[2]).transpose())

    # Plot the TM as a binary image
    plt.imshow(tm_array, cmap='binary', interpolation='nearest')

    # Show the plot
    plt.show()
