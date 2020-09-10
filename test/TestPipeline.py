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

from simpa.utils import Tags
from simpa.core.volume_creation import create_muscle_background, create_epidermis_layer, create_vessel_tube
from simpa.core.simulation import simulate
import numpy as np
import os

VOLUME_WIDTH_IN_MM = 10
VOLUME_HEIGHT_IN_MM = 10
SPACING = 0.25
RANDOM_SEED = 4711


def create_example_tissue():
    """
    This is a very simple example script of how to create a tissue definition.
    It contains a muscular background, an epidermis layer on top of the muscles
    and a blood vessel.
    """
    tissue_dict = dict()
    tissue_dict["background"] = create_muscle_background()
    tissue_dict["epidermis"] = create_epidermis_layer()
    tissue_dict["vessel"] = create_vessel_tube(x_min=0, x_max=VOLUME_WIDTH_IN_MM,
                                               z_min=0, z_max=VOLUME_HEIGHT_IN_MM,
                                               r_min=1, r_max=3)
    return tissue_dict

# Seed the numpy random configuration prior to creating the settings file in
# order to ensure that the same volume
# is generated with the same random seed every time.

np.random.seed(RANDOM_SEED)

settings = {
    # These parameters set the general propeties of the simulated volume
    Tags.RANDOM_SEED: RANDOM_SEED,
    Tags.VOLUME_NAME: "TestName_"+str(RANDOM_SEED),
    Tags.SIMULATION_PATH: ".",
    Tags.SPACING_MM: SPACING,
    Tags.DIM_VOLUME_Z_MM: VOLUME_HEIGHT_IN_MM,
    Tags.DIM_VOLUME_X_MM: VOLUME_WIDTH_IN_MM,
    Tags.DIM_VOLUME_Y_MM: VOLUME_WIDTH_IN_MM,
    Tags.AIR_LAYER_HEIGHT_MM: 0,
    Tags.GELPAD_LAYER_HEIGHT_MM: 0,

    # The following parameters set the optical forward model
    Tags.RUN_OPTICAL_MODEL: True,
    Tags.WAVELENGTHS: [800],
    Tags.OPTICAL_MODEL_NUMBER_PHOTONS: 1e7,
    Tags.OPTICAL_MODEL: Tags.OPTICAL_MODEL_TEST,
    Tags.ILLUMINATION_TYPE: Tags.ILLUMINATION_TYPE_PENCIL,
    # Tags.LASER_PULSE_ENERGY_IN_MILLIJOULE: [50],

    # The following parameters tell the script that we do not want any extra
    # modelling steps
    Tags.PERFORM_UPSAMPLING: True,
    Tags.UPSCALE_FACTOR: 1,
    Tags.UPSAMPLING_METHOD: Tags.UPSAMPLING_METHOD_NEAREST_NEIGHBOUR,
    Tags.RUN_ACOUSTIC_MODEL: True,
    Tags.ACOUSTIC_MODEL: Tags.ACOUSTIC_MODEL_TEST,
    Tags.APPLY_NOISE_MODEL: True,
    Tags.NOISE_MODEL: Tags.NOISE_MODEL_GAUSSIAN,
    Tags.PERFORM_IMAGE_RECONSTRUCTION: True,
    Tags.RECONSTRUCTION_ALGORITHM: Tags.RECONSTRUCTION_ALGORITHM_TEST,
    Tags.SIMULATION_EXTRACT_FIELD_OF_VIEW: False,

    # Add the volume_creation to be simulated to the tissue
    Tags.STRUCTURES: create_example_tissue()
}
print("Simulating ", RANDOM_SEED)
simulate(settings)

if (os.path.exists(settings[Tags.SIMPA_OUTPUT_PATH]) and
        os.path.isfile(settings[Tags.SIMPA_OUTPUT_PATH])):
    # Delete the created file
    os.remove(settings[Tags.SIMPA_OUTPUT_PATH])
    path = ""
    for subpath in settings[Tags.SIMPA_OUTPUT_PATH].split("/")[:-1]:
        path += subpath + "/"
    # Delete the file's parent directory
    os.rmdir(path)

print("Simulating ", RANDOM_SEED, "[Done]")