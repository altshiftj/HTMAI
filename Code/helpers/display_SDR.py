import matplotlib.pyplot as plt
import math
import numpy as np

def display_SDR(SDR):
    # Make a 9x9 grid...

    nrows = int(math.sqrt(SDR.size))
    i=0
    while not SDR.size % nrows == 0:
        i+=1
        if SDR.size % (nrows+i) == 0:
            nrows = int(nrows + i)
            break
        elif SDR.size % (nrows-i) == 0:
            nrows = int(nrows - i)
            break

    ncols = int(SDR.size/nrows)
    image = np.zeros(SDR.size)

    # Set every other cell to a random number (this would be your data)
    image = SDR.dense

    # Reshape things into a 9x9 grid.
    image = image.reshape((nrows,ncols))


    plt.matshow(image)
    plt.show()