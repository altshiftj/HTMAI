import random
import numpy as np
from htm.bindings.sdr import SDR

def generate_random_sdr(dimensions, sparsity):
    # Create a new SDR with the specified dimensions
    sdr = SDR(dimensions=dimensions)

    # Choose a random set of indices for the active bits
    num_active_bits = int(np.prod(dimensions) * sparsity)
    active_indices = random.sample(range(np.prod(dimensions)), num_active_bits)

    # Set the active bits using the sparse attribute
    sdr.sparse = active_indices

    return sdr