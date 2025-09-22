"""
file: activities.py
To convert XCAT phantom into dynamic PET data
"""

import struct
import csv
import numpy as np
from matplotlib import pyplot as plt

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

    phantom = np.flip(phantom.reshape((z_size, x_size, y_size)), axis=0)

    return phantom

def readTAC(filename, verbose=True):
    if verbose:
        print(filename)

    time_vals = []
    TAC_vals = []

    try:
        with open(filename) as csvfile:
            lines_in = csv.reader(csvfile)
            line_number = 1
            for row in lines_in:
                if line_number > 1:
                    time_vals.append(float(row[0]))
                    TAC_vals.append(float(row[1]))
                line_number += 1

            if time_vals[0] > 1E-10:
                time_vals = np.concatenate((np.zeros(1), time_vals))
                TAC_vals = np.concatenate((np.zeros(1), TAC_vals))
    except IOError:
        print("TAC file not accessible")

    if verbose:
        plt.figure()
        plt.scatter(time_vals, TAC_vals, marker="o", color="k")
        plt.plot(time_vals, TAC_vals, color="r")
        plt.xlabel("Time (minutes)")
        plt.ylabel("Activity concentration")
        plt.show()

    return time_vals, TAC_vals
