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
sys.path.insert(0, '/home/pclegg/devel/SIRF-SuperBuild/docker/devel/IDIF/src')
import PET_tools as tpT

import sirf.STIR as tpPET

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

@pytest.mark.skip()
def test_addActivityToPhantom():
    data_stem = "/home/pclegg/devel/SIRF-SuperBuild/docker/devel/Dual/data"
    filename = "biograph_out_act_1.bin"
    path = os.path.join(data_stem, filename)
    nframes = 48
    phantom = tpA.readRawPhantomData(path, array=285, slices=127)
    dynamic = tpS.expandPhantomToFrames(phantom, nframes)

    organ_codes = np.linspace(1, 20, 20, dtype=int)
    filenames = ["Bone_FDG_FAPI_decay.csv", "Zero_FDG_FAPI_decay.csv", 
            "Zero_FDG_FAPI_decay.csv", 
            "Zero_FDG_FAPI_decay.csv", "Zero_FDG_FAPI_decay.csv", 
            "Pancreas_FDG_FAPI_decay.csv", "Liver_FDG_FAPI_decay.csv", 
            "Muscle_FDG_FAPI_decay.csv", "Zero_FDG_FAPI_decay.csv", 
            "Zero_FDG_FAPI_decay.csv", 
            "Blood_FDG_FAPI_decay.csv", 
            "Kidneys_FDG_FAPI_decay.csv", "Spleen_FDG_FAPI_decay.csv", 
            "Blood_FDG_FAPI_decay.csv", "Zero_FDG_FAPI_decay.csv", 
            "Myocardium_FDG_FAPI_decay.csv", "Zero_FDG_FAPI_decay.csv", 
            "Zero_FDG_FAPI_decay.csv",
            "Lungs_FDG_FAPI_decay.csv", "Bone_FDG_FAPI_decay.csv"]
    for code in organ_codes:
        name = filenames[code-1]
        if len(name) > 2:
            path = os.path.join(data_stem, name)
            time, activity = tpA.readTAC(path, verbose=False)
            if code < 20:
                dynamic = tpA.addActivityToDynamicPhantom(dynamic, code, 
                    activity, verbose=False)
            else:
                dynamic = tpA.addActivityToDynamicPhantom(dynamic, code, 
                    activity, verbose=True)

    out_name = os.path.join(data_stem, "first_decay_phantom.npy")
    tpS.writeDynamicPhantom(dynamic, out_name)

    assert True

@pytest.mark.skip()
def test_readAndSubsample():
    data_stem = "/home/pclegg/devel/SIRF-SuperBuild/docker/devel/Dual/data"
    in_file = "first_dual_phantom.npy"
    out_file = "short_single_injection_phantom.npy"
    in_name = os.path.join(data_stem, in_file)
    out_name = os.path.join(data_stem, out_file)
    num_frames = 29

    tpS.readAndSubsamplePhantom(in_name, num_frames, out_name)

    assert True

@pytest.mark.skip()
def test_createTemplate():
    tpS.createTemplate()

    assert True

@pytest.mark.skip()
def test_createAttenuationMap():
    data_stem = "/home/pclegg/devel/SIRF-SuperBuild/docker/devel/Dual/data"
    filename = "biograph_out_atn_1.bin"
    path = os.path.join(data_stem, filename)
    umap = tpA.readRawPhantomData(path, array=285, slices=127)

    out_name = os.path.join(data_stem, "phantom_umap.npy")
    sm_umap = np.array(umap, dtype=np.float32)
    np.save(out_name, sm_umap)

    assert True

@pytest.mark.skip()
def test_createTemplate():
    data_stem = "/home/pclegg/devel/SIRF-SuperBuild/docker/devel/Dual/data"
    tpT.create3Dtemplate(data_stem)

    assert True

#@pytest.mark.skip()
def test_createOneSinogramAtATime():
    Array = 285
    Slices = 127
    data_stem = "/home/pclegg/devel/SIRF-SuperBuild/docker/devel/Dual/data"
    in_file = "first_decay_phantom.npy"
    in_name = os.path.join(data_stem, in_file)

    norm_file = "attempt2a.n.hdr"
    norm_name = os.path.join(data_stem, norm_file)

    template_path = os.path.join(data_stem, "template3D.hs")
    template = tpPET.AcquisitionData(template_path)
    im_pet = tpPET.ImageData(template)

    umap_file = "biograph_out_atn_1.bin"
    umap_name = os.path.join(data_stem, umap_file)

    umap_raw = tpA.readRawPhantomData(umap_name, array=Array, slices=Slices)
    umap_raw *= 4.75

    example_file = "SinoSet1_ISTA_image.hv"
    example_name = os.path.join(data_stem, example_file)
    example_image = tpPET.ImageData(example_name)

    attn_image = example_image.clone()
    attn_image.fill(umap_raw)

    image_data = example_image.clone()
    num_frames = 48
    out_data = np.zeros((num_frames, Slices, Array, Array))
    print("\n")
    for frame in range(num_frames):
        image_raw = tpS.returnOneFrame(in_name, frame)
        image_data.fill(image_raw)
        print(frame)
        acq_data = tpT.imageToSinogram(image_data, template, 
                attn_image, norm_name)
        image_out = tpT.reconstructRawPhantomPET(acq_data, template, 
                attn_image, norm_name)
        out_data[frame, :, :, :] = image_out.as_array()

    out_file = "Decay_Analytical.npy"
    out_name = os.path.join(data_stem, out_file)
    tpS.writeDynamicPhantom(out_data, out_name)

    assert True

