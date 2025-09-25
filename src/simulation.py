"""
file: simulation.py
To create an analytical simulation of the XCAT phantom
"""

import numpy as np
from matplotlib import pyplot as plt

def displayPhantom(phantom, verbose=True):
    x_mid = phantom.shape[1] // 2
    if verbose:
        print(f"Slice: {x_mid}")

    plt.figure()
    plt.imshow(phantom[:, x_mid, :])
    plt.show()

def expandPhantomToFrames(phantom, nframes, verbose=True):
    if verbose:
        print(phantom.shape)

    (nslices, x_size, y_size) = phantom.shape

    dynamic = np.zeros((nframes, nslices, x_size, y_size))

    dynamic[:, :, :, :] = phantom

    if verbose:
        print(dynamic.shape)

    return dynamic

def writeDynamicPhantom(dynamic, filename):
    np.save(filename, dynamic)



