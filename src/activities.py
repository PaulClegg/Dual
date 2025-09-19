"""
file: activities.py
To convert XCAT phantom into dynamic PET data
"""

import struct
import numpy as np

def readRawPhantomData(filename, verbose=True):
    if verbose:
        print(filename)

    size = 4
    x_size = 256; y_size = 256; z_size = 301
    phantom = np.zeros(x_size * y_size * z_size)

    i = 0
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(size)
            if not chunk:
                 break

            phantom[i] = struct.unpack("<f", chunk)[0]
            i = i + 1

        f.close()

    phantom = phantom.reshape((x_size, y_size, z_size))

    return phantom
