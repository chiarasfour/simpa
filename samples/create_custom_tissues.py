# The MIT License (MIT)
#
# Copyright (c) 2018 Computer Assisted Medical Interventions Group, DKFZ
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from simpa.utils import TissueSettingsGenerator
from simpa.utils import CHROMOPHORE_LIBRARY
from simpa.utils import Chromophore
from simpa.utils import AbsorptionSpectrum
import numpy as np


def create_custom_absorber():
    wavelengths = np.linspace(200, 1500, 100)
    absorber = AbsorptionSpectrum(spectrum_name="random absorber",
                                  wavelengths=wavelengths,
                                  absorption_per_centimeter=np.random.random(
                                      np.shape(wavelengths)))
    return absorber


def create_custom_chromophore(volume_fraction: float = 1.0):
    chromophore = Chromophore(
            spectrum=create_custom_absorber(),
            volume_fraction=volume_fraction,
            mus500=40.0,
            b_mie=1.1,
            f_ray=0.9,
            anisotropy=0.9
        )
    return chromophore


def create_custom_tissue_type():

    # First create an instance of a TissueSettingsGenerator
    tissue_settings_generator = TissueSettingsGenerator()

    water_volume_fraction = 0.4
    bvf = 0.5
    oxy = 0.4

    # Then append chromophores that you want
    tissue_settings_generator.append(key="oxyhemoglobin", value=
                            CHROMOPHORE_LIBRARY.oxyhemoglobin(oxy*bvf))
    tissue_settings_generator.append(key="deoxyhemoglobin", value=
                            CHROMOPHORE_LIBRARY.deoxyhemoglobin(oxy * bvf))
    tissue_settings_generator.append(key="water", value=
                            CHROMOPHORE_LIBRARY.water(water_volume_fraction))
    tissue_settings_generator.append(key="custom", value=
                            create_custom_chromophore(0.1))

    return tissue_settings_generator.get_settings()
