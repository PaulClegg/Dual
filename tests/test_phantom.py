"""
file: test_phantom.py
Tests of XCAT phantom functions
"""

import pytest
import sys
import os
import numpy as np

sys.path.insert(0, '/home/pclegg/devel/SIRF-SuperBuild/docker/devel/Dual/src')
import activities as tpA
import simulation as tpS

@pytest.mark.skip()
def test_readingRawPhantomData():
    filename = "coded_out_act_1.bin"
    data_stem = "/home/pclegg/devel/SIRF-SuperBuild/docker/devel/Dual/data"
    path = os.path.join(data_stem, filename)

    phantom = tpA.readRawPhantomData(path)
    tpS.displayPhantom(phantom)

    assert True

@pytest.mark.skip()
def test_readingFramedActivities():
    act_file = "FDG_liver_framed.csv"
    data_stem = "/home/pclegg/devel/SIRF-SuperBuild/docker/devel/Dual/data"
    path = os.path.join(data_stem, act_file)

    time, activity = tpA.readTAC(path, verbose=True)

    assert True

@pytest.mark.skip()
def test_expandPhantomToFrames():
    filename = "coded_out_act_1.bin"
    data_stem = "/home/pclegg/devel/SIRF-SuperBuild/docker/devel/Dual/data"
    path = os.path.join(data_stem, filename)

    nframes = 24

    phantom = tpA.readRawPhantomData(path)
    dynamic = tpS.expandPhantomToFrames(phantom, nframes)

    assert True

@pytest.mark.skip()
def test_addLiverActivityToPhantom():
    act_file = "FDG_liver_framed.csv"
    data_stem = "/home/pclegg/devel/SIRF-SuperBuild/docker/devel/Dual/data"
    path = os.path.join(data_stem, act_file)
    time, activity = tpA.readTAC(path, verbose=True)

    filename = "coded_out_act_1.bin"
    path = os.path.join(data_stem, filename)
    nframes = len(time)
    phantom = tpA.readRawPhantomData(path)
    dynamic = tpS.expandPhantomToFrames(phantom, nframes)

    organ_code = 7
    dynamic = tpA.addActivityToDynamicPhantom(dynamic, organ_code, activity)

    out_name = os.path.join(data_stem, "first_dynamic_phantom.npy")
    tpS.writeDynamicPhantom(dynamic, out_name)

    assert True

#@pytest.mark.skip()
def test_addFDGActivityToPhantom():
    data_stem = "/home/pclegg/devel/SIRF-SuperBuild/docker/devel/Dual/data"
    filename = "coded_out_act_1.bin"
    path = os.path.join(data_stem, filename)
    nframes = 24
    phantom = tpA.readRawPhantomData(path)
    dynamic = tpS.expandPhantomToFrames(phantom, nframes)

    organ_codes = np.linspace(1, 18, 18, dtype=int)
    filenames = ["FDG_bone_framed.csv", "", "", "", "", 
            "FDG_pancreas_framed.csv", "FDG_liver_framed.csv", 
            "FDG_muscle_framed.csv", "", "", 
            "FDG_cleanbolus_framed.csv", 
            "FDG_kidneys_framed.csv", "FDG_spleen_framed.csv", 
            "FDG_cleanbolus_framed.csv", "", 
            "FDG_myocardium_framed.csv", "", ""]
    for code in organ_codes:
        name = filenames[code-1]
        if len(name) > 2:
            path = os.path.join(data_stem, name)
            time, activity = tpA.readTAC(path, verbose=False)
            if code < 16:
                dynamic = tpA.addActivityToDynamicPhantom(dynamic, code, 
                    activity, verbose=False)
            else:
                dynamic = tpA.addActivityToDynamicPhantom(dynamic, code, 
                    activity, verbose=True)

    out_name = os.path.join(data_stem, "first_dynamic_phantom.npy")
    tpS.writeDynamicPhantom(dynamic, out_name)

    assert True

