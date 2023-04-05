import htm
from htm.algorithms import SpatialPooler as SP
from htm.algorithms import TemporalMemory as TM
import htm.bindings.encoders as enc
from htm.bindings.sdr import *

import time
import math
import random
import networkx as nx

from Code.helpers.encode_helper import *
from Code.helpers.plot_sdr import *
from Code.helpers.topology_helpers import *
from Code.helpers.matrix_tests import *


random.seed(42)


def pool(pooler, active_columns, input_SDR, learning, metrics):
    """Function pool computes active columns of a temporal layer"""
    pooler.compute(input_SDR, learning, active_columns)
    metrics.addData(active_columns)

    return

def feedforward_memory(tm, active_columns, learning, metrics_to):
    """Function feedforward_memory recieves a temporal memory layer, its active columns, whether it learns or not
    and if metrics are to be recorded, and computes the current active and predictive cells"""
    tm.activateDendrites(learn=learning)
    tm.activateCells(active_columns, learn=learning)
    metrics_to.addData(tm.getActiveCells().flatten())

    return



def random_list(n, a, b):
    return [random.randint(a, b) for _ in range(n)]

list = random_list(4000, 0, 50)

NUMBER_OF_COLUMNS = 16
LAYER_DEPTH = 8
SDR_SIZE = [64,64]

encoder_parameters = rdse_encoder_parameters(
            # region Angle Encoder Parameters
            active_bits=0,
            category=0,
            radius=0,
            resolution=1,
            seed=1,
            size=SDR_SIZE[0]**2,
            sparsity=0.004,
            # endregion
        )

encoder = rdse_encoder(encoder_parameters)
sdr = SDR(SDR_SIZE)

sp = SP(
            # region L23_sp Parameters
            inputDimensions=SDR_SIZE,
            columnDimensions=[1,NUMBER_OF_COLUMNS],
            potentialRadius=SDR_SIZE[0],
            potentialPct=1,
            globalInhibition=True,
            localAreaDensity=.5,
            #numActiveColumnsPerInhArea=1,
            # stimulusThreshold=0,
            synPermConnected=0.7,
            synPermActiveInc=0.01,
            synPermInactiveDec=0.015,
            boostStrength=20,
            # minPctOverlapDutyCycle=0,
            # dutyCyclePeriod=0,
            # spVerbosity=0,
            wrapAround=False,
            seed=1,
            # endregion
        )
sp_info = Metrics(sp.getColumnDimensions(), 999999999)

sp_active_columns = SDR([1,NUMBER_OF_COLUMNS])

tm = TM(
    columnDimensions=sp.getColumnDimensions(),
    cellsPerColumn=LAYER_DEPTH,
    maxSegmentsPerCell=32,
    maxSynapsesPerSegment=32,
    maxNewSynapseCount=16,
    activationThreshold=9,
    minThreshold=6,
    initialPermanence=0.21,
    connectedPermanence=0.7,
    permanenceIncrement=0.1,
    permanenceDecrement=0.1,
    predictedSegmentDecrement=0.0,
    #externalPredictiveInputs=(number_of_columns * layer_depth),
    checkInputs=1,
    seed=10,
        )
tm_info = Metrics((tm.numberOfCells(),), 999999999)



# Turn on interactive mode
plt.ion()

# Create the figure with 3 rows and 1 column
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(5, 15))

time_start = time.time()

for i in list:
    encoder.encode(i, sdr)
    plot_2d_sdr(sdr)
    pool(sp, sp_active_columns, sdr, True, sp_info)
    feedforward_memory(tm, sp_active_columns, True, tm_info)
    a = tm.getActiveCells().reshape((LAYER_DEPTH, NUMBER_OF_COLUMNS))
    plot_2d_tm(tm)
    plot_2d_sdr_sp_tm(sdr, sp_active_columns, tm.getActiveCells(), fig, ax1, ax2, ax3)


time_end = time.time()

 in_deg_matrix, adj_matrix, in_laplace_matrix = get_graph_theory(tm)
#
#
# print("Time elapsed: ", time_end - time_start)
#
# test_matrix(in_deg_matrix)
# test_matrix(adj_matrix)
# test_matrix(in_laplace_matrix)
#
# plot_matrix(in_deg_matrix, "In Degree", "tm", LAYER_DEPTH, LAYER_DEPTH)
# spectrum = matrix_spectrum(in_deg_matrix)
# plot_eigenvalues(spectrum)
#
# plot_matrix(adj_matrix, "Adjacency", "tm", LAYER_DEPTH, LAYER_DEPTH)
# spectrum = matrix_spectrum(adj_matrix)
# plot_eigenvalues(spectrum)
#
# plot_matrix(in_laplace_matrix, "In Laplace", "tm", LAYER_DEPTH, LAYER_DEPTH)
# spectrum = matrix_spectrum(in_laplace_matrix)
# plot_eigenvalues(spectrum)
#
# a=1