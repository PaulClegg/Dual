"""
file: simulation.py
To create an analytical simulation of the XCAT phantom
"""

import numpy as np
from matplotlib import pyplot as plt
import nibabel as nib

import sirf.STIR as sPET

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
    dynamic *= 100.0
    sm_dynamic = np.array(dynamic, dtype=np.ushort)
    np.save(filename, sm_dynamic)

def readAndSubsamplePhantom(in_name, num_frames, out_name):
    lg_dynamic = np.load(in_name, encoding="bytes")
    dynamic = lg_dynamic[:num_frames, :, :, :]
    sm_dynamic = np.array(dynamic, dtype=np.ushort)
    np.save(out_name, sm_dynamic)

def createTemplate():
    #template_acq_data = sPET.AcquisitionData('Siemens_mMR', span=11,
    template_acq_data = sPET.AcquisitionData('Siemens_Biograph_Vision_Quadra', 
        span=11,
        max_ring_diff=15, view_mash_factor=2)
