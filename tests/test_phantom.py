"""
file: test_phantom.py
Tests of XCAT phantom functions
"""

import pytest
import sys
import os

sys.path.insert(0, '/home/pclegg/devel/SIRF-SuperBuild/docker/devel/Dual/src')
import activities as tpA
import simulation as tpS

#@pytest.mark.skip()
def test_readingRawPhantomData():
    filename = "coded_out_act_1.bin"
    data_stem = "/home/pclegg/devel/SIRF-SuperBuild/docker/devel/Dual/data"
    path = os.path.join(data_stem, filename)

    phantom = tpA.readRawPhantomData(path)
    tpS.displayPhantom(phantom)

    assert True
