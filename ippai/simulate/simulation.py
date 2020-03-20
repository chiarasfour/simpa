from ippai.simulate import Tags
from ippai.simulate.volume_creator import create_simulation_volume
from ippai.simulate.models.optical_modelling import run_optical_forward_model
from ippai.simulate.models.acoustic_modelling import run_acoustic_forward_model
from ippai.simulate.models.noise_modelling import apply_noise_model_to_reconstructed_data
from ippai.simulate.models.reconstruction import perform_reconstruction
from ippai.process.sampling import upsample
from ippai.io_handling.io_hdf5 import save_hdf5, load_hdf5
import numpy as np
import os


def simulate(settings):
    """

    :param settings:
    :return:
    """

    ippai_output = dict()
    wavelengths = settings[Tags.WAVELENGTHS]
    volume_output_paths = []
    optical_output_paths = []
    acoustic_output_paths = []
    reconstruction_output_paths = []

    path = settings[Tags.SIMULATION_PATH] + "/" + settings[Tags.VOLUME_NAME] + "/"
    if not os.path.exists(path):
        os.makedirs(path)

    ippai_output_path = path + "ippai_output.hdf5"

    ippai_output[Tags.SETTINGS] = settings
    save_hdf5(ippai_output, ippai_output_path)
    settings[Tags.IPPAI_OUTPUT_PATH] = ippai_output_path

    for wavelength in wavelengths:

        if settings[Tags.RANDOM_SEED] is not None:
            np.random.seed(settings[Tags.RANDOM_SEED])
        else:
            np.random.seed(None)

        settings[Tags.WAVELENGTH] = wavelength
        volume_output_path = create_simulation_volume(settings)
        volume_output_paths.append(volume_output_path)

        optical_output_path = None
        acoustic_output_path = None

        if settings[Tags.RUN_OPTICAL_MODEL]:
            optical_output_path = run_optical_forward_model(settings, volume_output_path)
            optical_output_paths.append(optical_output_path)

        if Tags.SIMULATION_EXTRACT_FIELD_OF_VIEW in settings:
            if settings[Tags.SIMULATION_EXTRACT_FIELD_OF_VIEW]:
                extract_field_of_view(settings, volume_output_path, optical_output_path, acoustic_output_path)

        if Tags.PERFORM_UPSAMPLING in settings:
            if settings[Tags.PERFORM_UPSAMPLING]:
                optical_output_path = upsample(settings, optical_output_path)
                optical_output_paths.append(optical_output_path)

        if Tags.RUN_ACOUSTIC_MODEL in settings:
            if settings[Tags.RUN_ACOUSTIC_MODEL]:
                acoustic_output_path = run_acoustic_forward_model(settings, optical_output_path)
                acoustic_output_paths.append(acoustic_output_path)

        if Tags.PERFORM_IMAGE_RECONSTRUCTION in settings:
            if settings[Tags.PERFORM_IMAGE_RECONSTRUCTION]:
                reconstruction_output_path = perform_reconstruction(settings, acoustic_output_path)
                if (Tags.APPLY_NOISE_MODEL in settings) and settings[Tags.APPLY_NOISE_MODEL]:
                    reconstruction_output_path = apply_noise_model_to_reconstructed_data(settings, reconstruction_output_path)
                reconstruction_output_paths.append(reconstruction_output_path)

    return [volume_output_paths, optical_output_paths, acoustic_output_paths, reconstruction_output_paths]


def extract_field_of_view(settings, volume_path, optical_path, acoustic_path):
    if volume_path is not None:
        volume_data = load_hdf5(settings[Tags.IPPAI_OUTPUT_PATH], volume_path)
        sizes = np.shape(volume_data[Tags.PROPERTY_ABSORPTION_PER_CM])
        for key, value in volume_data.items():
            if np.shape(value) == sizes:
                volume_data[key] = value[:, int(sizes[1]/2), :]

        save_hdf5(volume_data, settings[Tags.IPPAI_OUTPUT_PATH], volume_path)

    if optical_path is not None:
        optical_data = load_hdf5(settings[Tags.IPPAI_OUTPUT_PATH], optical_path)
        fluence = optical_data['fluence']
        sizes = np.shape(fluence)
        optical_data["fluence"] = fluence[:, int(sizes[1] / 2), :]
        optical_data['initial_pressure'] = optical_data['initial_pressure'][:, int(sizes[1] / 2), :]

        save_hdf5(optical_data, settings[Tags.IPPAI_OUTPUT_PATH], optical_path)


    if acoustic_path is not None:
        acoustic_data = np.load(acoustic_path)
