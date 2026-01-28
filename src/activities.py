"""
file: activities.py
To convert XCAT phantom into dynamic PET data
"""

import struct
import csv
import os
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

def uMapFromPhantom(data_path, in_name, out_name, atten_dict, verbose=True):
    path = os.path.join(data_path, in_name)
    phantom = readRawPhantomData(path, array=285, slices=127)

    # Key:
    #tissueprop(8)  = 'muscle'
    #tissueprop(19) = 'lungs'
    #tissueprop(1)  = 'bone'
    #tissueprop(2)  = 'fat'
    #tissueprop(3)  = 'skin'
    #tissueprop(4)  = 'colon'
    #tissueprop(5)  = 'gastro'
    #tissueprop(6)  = 'pancreas'
    #tissueprop(7)  = 'liver'
    #tissueprop(9)  = 'gallbladder'
    #tissueprop(10) = 'adrenalgland'
    #tissueprop(11) = 'vein'
    #tissueprop(12) = 'kidney'
    #tissueprop(13) = 'spleen'
    #tissueprop(14) = 'artery'
    #tissueprop(15) = 'ureter'
    #tissueprop(16) = 'myocardium'
    #tissueprop(17) = 'esophagus'
    #tissueprop(18) = 'lymph'
    #tissueprop(20) = 'bone marrow'

    organ_dict = {}
    organ_dict["lung"] = 19
    organ_dict["dry_spine"] = 1
    organ_dict["dry_rib"] = 1
    organ_dict["skull"] = 1
    organ_dict["adipose"] = 2
    organ_dict["skin"] = 3
    organ_dict["intestine"] = 5
    organ_dict["pancreas"] = 6
    organ_dict["liver"] = 7
    organ_dict["muscle"] = 8
    organ_dict["kidney"] = 12
    organ_dict["spleen"] = 13
    organ_dict["blood"] = 14
    organ_dict["heart"] = 16
    organ_dict["lymph"] = 18
    #organ_dict["cartilage"] = 0.10400932
    #organ_dict["brain"] = 0.099343632
    organ_dict["red_marrow"] = 20
    organ_dict["yellow_marrow"] = 20

    # I need to check whether organ exists in organ_dict
    # If it doesn't I should print it out - as this could help!

    for organ, attenuation in atten_dict.items():
        phantom[phantom == organ_dict[organ]] = attenuation

    if verbose:
        x_mid = phantom.shape[1] // 2
        plt.figure()
        plt.imshow(phantom[:, x_mid, :])
        plt.show()

        print(f"Minimum = {phantom.min()}")
        print(f"Maximum = {phantom.max()}")

    out_path = os.path.join(data_path, out_name)
    print(out_path)
    np.save(out_path, phantom)

    
