import htm
from htm.algorithms import SpatialPooler as SP
from htm.algorithms import TemporalMemory as TM
import htm.bindings.encoders as enc
from htm.bindings.sdr import *

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import scipy.sparse as sp
import math


def get_graph_theory(tm: TM):
    # Get the number of cells in the temporal memory
    num_cells = tm.numberOfCells()

    # Get the permanence threshold of the temporal memory network
    perm_limit = tm.getConnectedPermanence()

    # Create an empty degree matrix of size num_cells x num_cells
    in_deg_matrix = np.zeros((num_cells, num_cells))

    # Initialize an empty adjacency matrix with dimensions of num_cells x num_cells
    adj_matrix = np.zeros((num_cells, num_cells))

    # Initialize an empty laplacian matrix with dimensions of num_cells x num_cells
    in_laplacian_matrix = np.zeros((num_cells, num_cells))


    # Iterate over all the cells in the temporal memory
    for i in range(num_cells):
        # Get the segments for the current cell
        cell_segments = tm.connections.segmentsForCell(i)
        # Iterate over all the segments for the current cell
        for segment in cell_segments:
            # Get the synapses for the current segment
            segment_synapses = tm.connections.synapsesForSegment(segment)
            # Iterate over all the synapses for the current segment
            for synapse in segment_synapses:
                # Get the presynaptic cell for the current synapse
                presynaptic_cell = tm.connections.presynapticCellForSynapse(synapse)
                # Get the permanence of the current synapse
                syn_perm = tm.connections.permanenceForSynapse(synapse)
                # If the permanence is greater than the connected permanence threshold, the synapse is connected
                # and we add an edge to the adjacency matrix
                if syn_perm >= perm_limit:
                    adj_matrix[presynaptic_cell, i] = 1
                    in_deg_matrix[i, i] += 1
                else:
                    adj_matrix[i, presynaptic_cell] = 0

    # Populate the laplacian matrix, L = D - A
    in_laplacian_matrix = in_deg_matrix - adj_matrix

    return  in_deg_matrix, adj_matrix, in_laplacian_matrix

# Function to update adjacency matrix
def update_adjacency_matrix(adj_matrix: np.array, tm: TM):
    for i in range(num_cells):
        # Get the segments for the current cell
        cell_segments = tm.connections.segmentsForCell(i)
        # Iterate over all the segments for the current cell
        for segment in cell_segments:
            # Get the synapses for the current segment
            segment_synapses = tm.connections.synapsesForSegment(segment)
            # Iterate over all the synapses for the current segment
            for synapse in segment_synapses:
                # Get the presynaptic cell for the current synapse
                presynaptic_cell = tm.connections.presynapticCellForSynapse(synapse)
                # Get the permanence of the current synapse
                syn_perm = tm.connections.permanenceForSynapse(synapse)
                # If the permanence is greater than the connected permanence threshold, the synapse is connected
                # and we add an edge to the adjacency matrix
                if syn_perm >= perm_limit:
                    adj_matrix[i, presynaptic_cell] = 1
                else:
                    adj_matrix[i, presynaptic_cell] = 0


def plot_matrix(matrix: np.array, matrix_name: str, tm_name: str, xticks: int, yticks: int):
    fig1 = plt.figure()
    plt.imshow(matrix, cmap='binary', interpolation='nearest')
    plt.title("{} Matrix for {}".format(matrix_name, tm_name))
    plt.grid(True, which='both', color='0.65', linestyle='-', linewidth=1)
    plt.xticks(np.arange(xticks, matrix.shape[0], xticks))
    plt.yticks(np.arange(yticks, matrix.shape[1], yticks))
    plt.xlabel("Output Cells"), plt.ylabel("Input Cells")
    plt.show()
    plt.waitforbuttonpress()
    plt.close()

def tm_adjacency_matrix_to_graph(tm: TM, tm_name: str):
    adj_matrix = get_graph_theory(tm)
    G = nx.from_numpy_array(adj_matrix, create_using=nx.DiGraph)
    return G

def matrix_spectrum(matrix: np.array):

    # Get the eigenvalues of the adjacency matrix
    eigenvalues = np.linalg.eigvals(matrix)
    return eigenvalues

def plot_eigenvalues(eigenvalues: np.array):

    # Create the scatter plot
    fig, ax = plt.subplots()
    ax.scatter(np.real(eigenvalues), np.imag(eigenvalues), c = np.sqrt(abs(eigenvalues)), cmap='viridis', alpha=0.5)

    # Add axis labels and a title
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    ax.set_title('Eigenvalues')

    # Show the plot
    plt.show()
    plt.waitforbuttonpress()
    plt.close()
