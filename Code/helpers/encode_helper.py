import htm.bindings.encoders as e

def scalar_encoder_parameters(
                              active_bits,
                              category,
                              clip_input,
                              maximum,
                              minimum,
                              periodic,
                              radius,
                              resolution,
                              size,
                              sparsity
                            ):
    """
    A helper function to encapsulate the parameters of an encoder.
    """
    parameters = e.ScalarEncoderParameters()

    parameters.activeBits   = active_bits
    parameters.category     = category
    parameters.clipInput    = clip_input
    parameters.maximum      = maximum
    parameters.minimum      = minimum
    parameters.periodic     = periodic
    parameters.radius       = radius
    parameters.resolution   = resolution
    parameters.size         = size
    parameters.sparsity     = sparsity

    return parameters


def scalar_encoder(parameters):
    """
    Creates a ScalarEncoder object with the given parameters.
    """
    scalar_encoder = e.ScalarEncoder(parameters)

    return scalar_encoder


def rdse_encoder_parameters(
                            active_bits,
                            category,
                            radius,
                            resolution,
                            seed,
                            size,
                            sparsity
                           ):
    """
    A helper function to encapsulate the parameters of an RDSE encoder.
    """
    parameters = e.RDSE_Parameters()

    parameters.activeBits   = active_bits
    parameters.category     = category
    parameters.radius       = radius
    parameters.resolution   = resolution
    parameters.seed         = seed
    parameters.size         = size
    parameters.sparsity     = sparsity

    return parameters


def rdse_encoder(parameters):
    """
    Creates a RDSE object with the given parameters.
    """
    rdse_encoder = e.RDSE(parameters)

    return rdse_encoder
