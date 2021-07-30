"""
SPDX-FileCopyrightText: 2021 Computer Assisted Medical Interventions Group, DKFZ
SPDX-FileCopyrightText: 2021 VISION Lab, Cancer Research UK Cambridge Institute (CRUK CI)
SPDX-License-Identifier: MIT
"""

from simpa.core.reconstruction_module import ReconstructionAdapterBase


class ReconstructionModuleTestAdapter(ReconstructionAdapterBase):

    def reconstruction_algorithm(self, time_series_sensor_data, detection_geometry):
        return time_series_sensor_data / 10 + 5
