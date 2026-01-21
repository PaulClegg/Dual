"""
file: activities.py
To convert XCAT phantom into dynamic PET data
"""

import struct
import csv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as ani
import matplotlib.cm as cm

def readRawPhantomData(filename, array=256, slices=301, verbose=True):
    if verbose:
        print(filename)

    size = 4
    x_size = array; y_size = array; z_size = slices
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

def addActivityToDynamicPhantom(dynamic, organ_code, activity, verbose=True):
    (nframes, _, _, _) = dynamic.shape
    assert nframes == len(activity), "activities: inconsistent framing!"

    if verbose:
        print(f"Organ code: {organ_code}")

    for frame in range(nframes):
        if verbose:
            print(f"Frame number: {frame + 1}")
        snapshot = dynamic[frame, :, :, :]
        snapshot[snapshot == organ_code] = activity[frame]
        dynamic[frame, :, :, :] = snapshot

    if verbose:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect('equal')
        ax.axis('off')
        x_mid = dynamic.shape[2] // 2
        dynamic[:, 0, x_mid, 0] = 45.0 # to set range on colour scale
        im = ax.imshow(dynamic[0, :, x_mid, :], cmap=cm.Greys_r,
                interpolation='nearest')
        plt.tight_layout()
        def update_frame(n):
            X = dynamic[n, :, x_mid, :]
            im.set_array(X)
        anim = ani.FuncAnimation(fig, update_frame, frames=nframes, 
                interval=1000, repeat=False)
        plt.show()
        dynamic[:, 0, x_mid, 0] = 0.0 # reset

    return dynamic

def readAttenuation(filename, verbose=True):
    if verbose:
        print(filename)

    organ_names = []
    attenuations = []
    
    try:
        with open(filename) as csvfile:
            lines_in = csv.reader(csvfile)
            line_number = 1
            for row in lines_in:
                entry_list = row[0].split("\t")
                if line_number > 1:
                    entry_list.remove("")
                if line_number == 1 or entry_list[0] == "511.0":
                    if line_number == 1:
                        organ_names = entry_list
                    else:
                        for val in entry_list:
                            attenuations.append(float(val))

                line_number += 1

    except IOError:
        print("Attenuation file not accessible")

    attenuation_dict = {}
    for name, atten in zip(organ_names, attenuations):
        attenuation_dict[name] = atten

    return attenuation_dict

#def uMapFromPhantom(
#        snapshot[snapshot == organ_code] = activity[frame]
