from ippai.simulate import Tags
from ippai.simulate.models.reconstruction_models.MitkBeamformingAdapter import MitkBeamformingAdapter
from ippai.io_handling.io_hdf5 import save_hdf5
import numpy as np


def perform_reconstruction(settings, acoustic_data_path):
    print("ACOUSTIC FORWARD")

    reconstructed_data_save_path = (settings[Tags.SIMULATION_PATH] + "/" + settings[Tags.VOLUME_NAME] + "/" +
                                    Tags.RECONSTRUCTION_OUTPUT_NAME + "_" + str(settings[Tags.WAVELENGTH]) + ".npz")

    reconstruction_method = None

    if ((settings[Tags.RECONSTRUCTION_ALGORITHM] == Tags.RECONSTRUCTION_ALGORITHM_DAS) or
        (settings[Tags.RECONSTRUCTION_ALGORITHM] == Tags.RECONSTRUCTION_ALGORITHM_DMAS) or
            (settings[Tags.RECONSTRUCTION_ALGORITHM] == Tags.RECONSTRUCTION_ALGORITHM_SDMAS)):
        reconstruction_method = MitkBeamformingAdapter()

    reconstruction = reconstruction_method.simulate(settings, acoustic_data_path)

    save_hdf5({"reconstructed_data": reconstruction}, settings[Tags.IPPAI_OUTPUT_PATH],
              "/simulations/upsampled/reconstruction/")

    return "/simulations/upsampled/reconstruction/"
